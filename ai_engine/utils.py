<<<<<<< HEAD
# import google.generativeai as genai
# from django.conf import settings

# genai.configure(api_key=settings.GEMINI_API_KEY)
# # model = genai.GenerativeModel('gemini-1.5-flash')
# model = genai.GenerativeModel("gemini-2.0-flash")

# def screen_resume(resume_text, job_description, job_skills):
#     prompt = f"""
#     You are an expert HR recruiter. Analyze this resume against the job description and give a match score.

#     JOB DESCRIPTION:
#     {job_description}

#     REQUIRED SKILLS:
#     {job_skills}

#     CANDIDATE RESUME:
#     {resume_text}

#     Respond in this exact format:
#     SCORE: [number between 0-100]
#     SUMMARY: [2-3 sentences about the candidate]
#     STRENGTHS: [bullet points of matching skills]
#     GAPS: [bullet points of missing skills]
#     RECOMMENDATION: [Shortlist / Review / Reject]
#     """
#     response = model.generate_content(prompt)
#     return parse_screening_result(response.text)

# def parse_screening_result(text):
#     result = {
#         'score': 0,
#         'summary': '',
#         'strengths': '',
#         'gaps': '',
#         'recommendation': ''
#     }
#     lines = text.strip().split('\n')
#     for line in lines:
#         if line.startswith('SCORE:'):
#             try:
#                 result['score'] = float(line.replace('SCORE:', '').strip())
#             except:
#                 result['score'] = 0
#         elif line.startswith('SUMMARY:'):
#             result['summary'] = line.replace('SUMMARY:', '').strip()
#         elif line.startswith('STRENGTHS:'):
#             result['strengths'] = line.replace('STRENGTHS:', '').strip()
#         elif line.startswith('GAPS:'):
#             result['gaps'] = line.replace('GAPS:', '').strip()
#         elif line.startswith('RECOMMENDATION:'):
#             result['recommendation'] = line.replace('RECOMMENDATION:', '').strip()
#     return result

# def generate_job_description(title, skills, experience, job_type, location):
#     prompt = f"""
#     You are an expert HR professional. Write a professional job description for this role.

#     Job Title: {title}
#     Required Skills: {skills}
#     Experience Level: {experience}
#     Job Type: {job_type}
#     Location: {location}

#     Write a complete job description with:
#     1. About the Role (2-3 sentences)
#     2. Key Responsibilities (5-6 bullet points)
#     3. Requirements (4-5 bullet points)
#     4. Nice to Have (3 bullet points)
#     5. What We Offer (3-4 bullet points)

#     Keep it professional, engaging and realistic.
#     """
#     response = model.generate_content(prompt)
#     return response.text

# def match_skills(candidate_skills, job_skills):
#     candidate_list = [s.strip().lower() for s in candidate_skills.split(',')]
#     job_list = [s.strip().lower() for s in job_skills.split(',')]
#     matched = [s for s in candidate_list if any(s in j or j in s for j in job_list)]
#     missing = [s for s in job_list if not any(s in c or c in s for c in candidate_list)]
#     score = (len(matched) / len(job_list) * 100) if job_list else 0
#     return {
#         'score': round(score, 1),
#         'matched': matched,
#         'missing': missing,
#         'total_required': len(job_list),
#         'total_matched': len(matched)
#     }




import google.generativeai as genai
from django.conf import settings
import re

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# ─────────────────────────────────────────────
# Resume Screening
# ─────────────────────────────────────────────

def screen_resume(resume_text, job_description, job_skills):
    prompt = f"""
You are an expert HR recruiter. Analyze this resume against the job description and give a match score.

JOB DESCRIPTION:
{job_description}

REQUIRED SKILLS:
{job_skills}

CANDIDATE RESUME:
{resume_text}

Respond using EXACTLY this format (each section may span multiple lines):

SCORE: [number between 0-100]
SUMMARY: [2-3 sentences about the candidate]
STRENGTHS:
[bullet points of matching skills, one per line starting with -]
GAPS:
[bullet points of missing skills, one per line starting with -]
RECOMMENDATION: [Shortlist / Review / Reject]
"""
    response = model.generate_content(prompt)
    return parse_screening_result(response.text)


# ── FIX 4: Multi-line aware parser ──
=======
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

>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
def parse_screening_result(text):
    result = {
        'score': 0,
        'summary': '',
        'strengths': '',
        'gaps': '',
        'recommendation': ''
    }
<<<<<<< HEAD

    # Extract SCORE
    score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', text)
    if score_match:
        result['score'] = float(score_match.group(1))

    # Extract RECOMMENDATION
    rec_match = re.search(r'RECOMMENDATION:\s*(.+)', text)
    if rec_match:
        result['recommendation'] = rec_match.group(1).strip()

    # Extract SUMMARY (single or multi-line, ends at next section)
    summary_match = re.search(
        r'SUMMARY:\s*(.*?)(?=\nSTRENGTHS:|\nGAPS:|\nRECOMMENDATION:|\Z)',
        text, re.DOTALL
    )
    if summary_match:
        result['summary'] = summary_match.group(1).strip()

    # Extract STRENGTHS block (multi-line)
    strengths_match = re.search(
        r'STRENGTHS:\s*(.*?)(?=\nGAPS:|\nRECOMMENDATION:|\Z)',
        text, re.DOTALL
    )
    if strengths_match:
        result['strengths'] = strengths_match.group(1).strip()

    # Extract GAPS block (multi-line)
    gaps_match = re.search(
        r'GAPS:\s*(.*?)(?=\nRECOMMENDATION:|\Z)',
        text, re.DOTALL
    )
    if gaps_match:
        result['gaps'] = gaps_match.group(1).strip()

    return result
# ── END FIX 4 ──


# ─────────────────────────────────────────────
# Job Description Generator
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# Skill Matcher — FIX 3: Now uses Gemini AI
# ─────────────────────────────────────────────

def match_skills(candidate_skills, job_skills):
    """
    Uses Gemini to semantically match candidate skills against job requirements.
    Falls back to string matching if the AI call fails.
    """
    candidate_list = [s.strip() for s in candidate_skills.split(',') if s.strip()]
    job_list = [s.strip() for s in job_skills.split(',') if s.strip()]

    if not job_list:
        return {
            'score': 0,
            'matched': [],
            'missing': [],
            'total_required': 0,
            'total_matched': 0,
            'ai_insight': 'No required skills specified for this job.'
        }

    prompt = f"""
You are a technical recruiter evaluating a candidate's skills against job requirements.

CANDIDATE SKILLS:
{', '.join(candidate_list)}

REQUIRED JOB SKILLS:
{', '.join(job_list)}

Instructions:
1. Consider synonyms and related technologies as matches (e.g. "ReactJS" matches "React", "Postgres" matches "PostgreSQL").
2. Identify which required skills the candidate has (matched) and which are missing.
3. Give an overall match score out of 100.
4. Write a 2-sentence insight about the candidate's fit.

Respond in EXACTLY this format:

SCORE: [0-100]
MATCHED: [comma-separated list of matched skills, or "None"]
MISSING: [comma-separated list of missing skills, or "None"]
INSIGHT: [2-sentence analysis]
"""

    try:
        response = model.generate_content(prompt)
        return parse_skill_match_result(response.text, job_list)
    except Exception:
        # Fallback to string matching if Gemini fails
        return _string_match_fallback(candidate_list, job_list)


def parse_skill_match_result(text, job_list):
    result = {
        'score': 0,
        'matched': [],
        'missing': [],
        'total_required': len(job_list),
        'total_matched': 0,
        'ai_insight': ''
    }

    score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', text)
    if score_match:
        result['score'] = round(float(score_match.group(1)), 1)

    matched_match = re.search(r'MATCHED:\s*(.+)', text)
    if matched_match:
        raw = matched_match.group(1).strip()
        result['matched'] = [] if raw.lower() == 'none' else [s.strip() for s in raw.split(',') if s.strip()]

    missing_match = re.search(r'MISSING:\s*(.+)', text)
    if missing_match:
        raw = missing_match.group(1).strip()
        result['missing'] = [] if raw.lower() == 'none' else [s.strip() for s in raw.split(',') if s.strip()]

    insight_match = re.search(r'INSIGHT:\s*(.+)', text)
    if insight_match:
        result['ai_insight'] = insight_match.group(1).strip()

    result['total_matched'] = len(result['matched'])
    return result


def _string_match_fallback(candidate_list, job_list):
    """Simple string overlap fallback when Gemini is unavailable."""
    c_lower = [s.lower() for s in candidate_list]
    j_lower = [s.lower() for s in job_list]
    matched = [j for j in job_list if any(j.lower() in c or c in j.lower() for c in c_lower)]
    missing = [j for j in job_list if j not in matched]
    score = round((len(matched) / len(job_list)) * 100, 1) if job_list else 0
    return {
        'score': score,
        'matched': matched,
        'missing': missing,
        'total_required': len(job_list),
        'total_matched': len(matched),
        'ai_insight': 'AI insight unavailable — showing basic skill match.'
    }

=======
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
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
