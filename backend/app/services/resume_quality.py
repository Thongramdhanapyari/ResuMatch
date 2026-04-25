from app.services.analyzer import extract_text, calculate_ats_score


WEAK_WORDS = [
    "hardworking", "passionate", "good", "nice", "responsible",
    "team player", "quick learner"
]

ACTION_WORDS = [
    "built", "developed", "created", "implemented", "designed",
    "optimized", "deployed", "improved", "managed", "led",
    "integrated", "automated"
]

COMMON_SECTIONS = [
    "skills", "education", "projects", "experience",
    "summary", "certifications"
]


async def analyze_resume_quality(file):
    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "analysis_type": "resume_quality",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "semantic_score": 0,
            "spelling_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not extract text from resume."],
        }

    resume_lower = resume_text.lower()
    words = resume_text.split()
    word_count = len(words)

    suggestions = []

    missing_sections = [
        section for section in COMMON_SECTIONS
        if section not in resume_lower
    ]

    if missing_sections:
        suggestions.append(
            "Missing important sections: " + ", ".join(missing_sections)
        )

    if word_count < 150:
        suggestions.append("Resume is too short. Add more project, skill, and impact details.")

    if word_count > 900:
        suggestions.append("Resume may be too long. Keep it concise and focused.")

    if "@" not in resume_text:
        suggestions.append("Add a professional email address.")

    if not any(word in resume_lower for word in ACTION_WORDS):
        suggestions.append("Use stronger action verbs like built, developed, implemented, deployed, or optimized.")

    weak_found = [word for word in WEAK_WORDS if word in resume_lower]

    if weak_found:
        suggestions.append(
            "Avoid weak/generic words: " + ", ".join(weak_found)
        )

    spelling_issues = []

    for word in words:
        clean = word.strip(".,()[]{}:-").lower()

        if len(clean) > 12 and clean.isalpha():
            spelling_issues.append(clean)

    spelling_issues = list(set(spelling_issues))[:10]

    spelling_score = max(0, 100 - len(spelling_issues) * 5)

    semantic_score = 100

    if not any(word in resume_lower for word in ACTION_WORDS):
        semantic_score -= 25

    if "project" not in resume_lower and "experience" not in resume_lower:
        semantic_score -= 25

    if not any(char.isdigit() for char in resume_text):
        semantic_score -= 20
        suggestions.append("Add numbers/metrics like improved speed by 30%, handled 100+ users, or reduced time by 40%.")

    ats_score = calculate_ats_score(resume_text)
    content_score = max(0, 100 - len(suggestions) * 8)

    final_score = round(
        (ats_score * 0.35)
        + (semantic_score * 0.30)
        + (spelling_score * 0.20)
        + (content_score * 0.15),
        2
    )

    return {
        "analysis_type": "resume_quality",
        "match_score": final_score,
        "skills_score": 0,
        "content_score": content_score,
        "ats_score": ats_score,
        "semantic_score": semantic_score,
        "spelling_score": spelling_score,
        "score_breakdown": {
            "ats_score": ats_score,
            "semantic_strength": semantic_score,
            "spelling_quality": spelling_score,
            "content_quality": content_score,
        },
        "matched_skills": [],
        "missing_skills": missing_sections,
        "spelling_issues": spelling_issues,
        "suggestions": suggestions or ["Resume quality looks good. Improve further with stronger metrics and impact."]
    }