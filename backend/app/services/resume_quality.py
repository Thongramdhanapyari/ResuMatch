from app.services.analyzer import extract_text
from app.utils.skill_extractor import extract_skills
from app.utils.section_parser import parse_sections
from app.utils.ats_checker import run_ats_checks


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
            "suggestions": ["Could not extract text from resume."],
            "parsed_sections": {},
            "section_confidence": {},
            "ats_details": {},
        }

    resume_lower = resume_text.lower()
    word_count = len(resume_text.split())

    parsed = parse_sections(resume_text)
    ats_result = run_ats_checks(resume_text)

    suggestions = []

    missing_sections = [
        section for section in COMMON_SECTIONS
        if section not in resume_lower
    ]

    if missing_sections:
        suggestions.append("Missing important sections: " + ", ".join(missing_sections))

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
        suggestions.append("Avoid weak/generic words: " + ", ".join(weak_found))

    spelling_score = 100

    semantic_score = 100

    if not any(word in resume_lower for word in ACTION_WORDS):
        semantic_score -= 20

    if "project" not in resume_lower:
        semantic_score -= 15

    if "experience" not in resume_lower:
        semantic_score -= 15

    if not any(char.isdigit() for char in resume_text):
        semantic_score -= 20
        suggestions.append(
            "Add numbers/metrics like improved speed by 30%, handled 100+ users, or reduced time by 40%."
        )

    semantic_score = max(0, semantic_score)

    resume_skills = extract_skills(resume_text)
    skills_score = min(100, len(resume_skills) * 5)

    if skills_score < 40:
        suggestions.append("Add more relevant technical skills to improve your profile.")

    content_score = max(0, 100 - len(suggestions) * 8)

    ats_score = ats_result["ats_score"]

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
        "skills_score": skills_score,
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
        "matched_skills": list(resume_skills),
        "suggestions": suggestions or [
            "Resume quality looks good. Improve further with stronger metrics and impact."
        ],
        "parsed_sections": parsed.get("sections", {}),
        "section_confidence": {
            k: round(v * 100, 2)
            for k, v in parsed.get("confidence", {}).items()
        },
        "ats_details": ats_result["details"],
    }