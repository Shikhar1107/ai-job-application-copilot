from app.ai.utils.json_parser import invoke_json_chain
from app.ai.prompts.interview_prep import INTERVIEW_PREP_SYSTEM_PROMPT
from app.schemas.analysis import InterviewQuestionsResult, InterviewQuestionsResponse, SingleInterviewQuestionResult

def generate_interview_questions(
        resume_text: str,
        job_description: str,
        fit_score: int,
        fit_summary: str,
        matched_skills: list[str],
        missing_skills: list[str],
) -> InterviewQuestionsResult:
    matched_skills_text = ", ".join(matched_skills) if matched_skills else None
    missing_skills_text = ", ".join(missing_skills) if missing_skills else None

    user_content = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Fit Score:
{fit_score}

Fit Summary:
{fit_summary}

Matched Skills:
{matched_skills_text}

Missing Skills:
{missing_skills_text}

Task:
Generate 8 to 12 interview preparation questions with strong suggested answers for this candidate and job.

Question mix:
- 3 to 4 questions based on matched skills
- 2 to 3 project-deep-dive questions based on resume experience
- 2 questions based on missing or weaker skills
- 1 to 2 behavioral or communication questions

For each interview question, return:
- question
- answer
- category
- difficulty
- evaluation_focus

Answer rules:
- Answers should be practical and interview-ready.
- Answers should be written from the candidate's perspective using "I" where appropriate.
- Do not falsely claim experience with missing skills.
- For missing skills, answer using adjacent experience and a clear learning/design approach.
- Keep each answer around 80 to 160 words.
- Return a JSON object with the key interview_questions.

Important:
- Do not assume the candidate has experience with missing skills.
- For missing skills, frame questions as conceptual or learning-gap questions.
- Return a JSON object with the key interview_questions.
"""

    return invoke_json_chain(
        schema=InterviewQuestionsResult,
        system_prompt=INTERVIEW_PREP_SYSTEM_PROMPT,
        user_content=user_content,
    )