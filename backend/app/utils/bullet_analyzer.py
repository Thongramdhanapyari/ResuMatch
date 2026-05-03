from app.ml.bullet_engine import analyze_bullet, extract_bullets


def analyze_bullets(text: str):
    bullets = extract_bullets(text)

    if not bullets:
        return {
            "bullet_score": 0,
            "analysis": [],
            "suggestions": ["No bullet points detected."]
        }

    results = [analyze_bullet(b) for b in bullets]

    # duplicate detection
    seen = set()
    duplicates = 0

    for r in results:
        norm = r["bullet"].lower()
        if norm in seen:
            duplicates += 1
        seen.add(norm)

    avg_score = sum(r["score"] for r in results) / len(results)
    avg_score = max(0, avg_score - duplicates * 5)

    suggestions = []

    if avg_score < 50:
        suggestions.append("Bullets are too vague or weak.")

    if any(r["vague"] for r in results):
        suggestions.append("Avoid vague phrases like 'worked on' or 'assisted in'.")

    if not any(r["has_outcome"] for r in results):
        suggestions.append("Add measurable impact (%, numbers, results).")

    if duplicates:
        suggestions.append("Avoid repeated or similar bullet points.")

    return {
        "bullet_score": round(avg_score, 2),
        "analysis": results,
        "suggestions": suggestions
    }