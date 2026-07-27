from .utils import (extract_skills,extract_experience,extract_education,)

def calculate_ats_score(resume_text, job):

    resume_skills = extract_skills(resume_text)
    experience = extract_experience(resume_text)
    education = extract_education(resume_text)
    score = 0

    # Skills 
    job_skills = []

    if job.skills:
        job_skills = [
            skill.strip().lower()
            for skill in job.skills.split(",")
        ]

    matched_skills = []

    for skill in resume_skills:
        if skill.lower() in job_skills:
            matched_skills.append(skill)

    if len(job_skills) > 0:
        score += (len(matched_skills) / len(job_skills)) * 60

    # Experience 
    required = job.experience

    if experience >= required:
        score += 25
    elif required > 0:
        score += (experience / required) * 25

    
    # Education 
    if education:
        score += 15


    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)
    print("Matched Skills:", matched_skills)
    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "experience": experience,
        "education": education,
    }