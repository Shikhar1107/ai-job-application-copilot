from app.schemas.analysis import SkillItem

def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())

def dedupe_strings(items: list[str]) -> list[str]:
    cleaned = []

    for item in items:
        value = item.strip()
        if value:
            cleaned.append(value)

    return sorted(set(cleaned), key=str.lower)

def dedupe_skill_items(skills: list[SkillItem]) -> list[SkillItem]:
    skill_map = {}

    for skill in skills:
        key = normalize_text(skill.canonical_name)
        if key and key not in skill_map:
            skill_map[key] = skill

    return list(skill_map.values())

def skill_names(skills: list[SkillItem]) -> list[str]:
    return dedupe_strings([skill.canonical_name for skill in skills])

def match_skills(
    resume_skills: list[SkillItem],
    job_skills: list[SkillItem],
) -> tuple[list[str], list[str]]:
    resume_canonical_names = {
        normalize_text(skill.canonical_name)
        for skill in resume_skills
    }

    matched = []
    missing = []

    for job_skill in job_skills:
        normalized_job_skill = normalize_text(job_skill.canonical_name)

        if normalized_job_skill in resume_canonical_names:
            matched.append(job_skill.canonical_name)
        else:
            missing.append(job_skill.canonical_name)

    return dedupe_strings(matched), dedupe_strings(missing)