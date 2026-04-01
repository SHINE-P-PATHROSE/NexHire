import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel("gemini-2.0-flash")

def screen_resume(resume_text, job_description, job_skills):
    prompt = f"""
    You are an expert HR recruiter. Analyze this resume against the job description and give a match score.

    JOB DESCRIPTION:
    {job_description}

    REQUIRED SKILLS:
    {job_skills}

    CANDIDATE RESUME:
    {resume_text}

    Respond in this exact format:
    SCORE: [number between 0-100]
    SUMMARY: [2-3 sentences about the candidate]
    STRENGTHS: [bullet points of matching skills]
    GAPS: [bullet points of missing skills]
    RECOMMENDATION: [Shortlist / Review / Reject]
    """
    response = model.generate_content(prompt)
    return parse_screening_result(response.text)

def parse_screening_result(text):
    result = {
        'score': 0,
        'summary': '',
        'strengths': '',
        'gaps': '',
        'recommendation': ''
    }
    lines = text.strip().split('\n')
    for line in lines:
        if line.startswith('SCORE:'):
            try:
                result['score'] = float(line.replace('SCORE:', '').strip())
            except:
                result['score'] = 0
        elif line.startswith('SUMMARY:'):
            result['summary'] = line.replace('SUMMARY:', '').strip()
        elif line.startswith('STRENGTHS:'):
            result['strengths'] = line.replace('STRENGTHS:', '').strip()
        elif line.startswith('GAPS:'):
            result['gaps'] = line.replace('GAPS:', '').strip()
        elif line.startswith('RECOMMENDATION:'):
            result['recommendation'] = line.replace('RECOMMENDATION:', '').strip()
    return result

def generate_job_description(title, skills, experience, job_type, location):
    prompt = f"""
    You are an expert HR professional. Write a professional job description for this role.

    Job Title: {title}
    Required Skills: {skills}
    Experience Level: {experience}
    Job Type: {job_type}
    Location: {location}

    Write a complete job description with:
    1. About the Role (2-3 sentences)
    2. Key Responsibilities (5-6 bullet points)
    3. Requirements (4-5 bullet points)
    4. Nice to Have (3 bullet points)
    5. What We Offer (3-4 bullet points)

    Keep it professional, engaging and realistic.
    """
    response = model.generate_content(prompt)
    return response.text

def match_skills(candidate_skills, job_skills):
    candidate_list = [s.strip().lower() for s in candidate_skills.split(',')]
    job_list = [s.strip().lower() for s in job_skills.split(',')]
    matched = [s for s in candidate_list if any(s in j or j in s for j in job_list)]
    missing = [s for s in job_list if not any(s in c or c in s for c in candidate_list)]
    score = (len(matched) / len(job_list) * 100) if job_list else 0
    return {
        'score': round(score, 1),
        'matched': matched,
        'missing': missing,
        'total_required': len(job_list),
        'total_matched': len(matched)
    }
