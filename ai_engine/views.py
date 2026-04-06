# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import JsonResponse
# from jobs.models import Job, Application
# from candidates.models import CandidateProfile
# from .utils import screen_resume, generate_job_description, match_skills
# import PyPDF2
# import io

# def extract_text_from_resume(resume_file):
#     try:
#         pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
#         text = ''
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#         return text
#     except:
#         return "Could not extract resume text"

# @login_required
# def screen_application(request, application_id):
#     if not request.user.is_employer():
#         messages.error(request, 'Employers only.')
#         return redirect('jobs:list')
#     application = get_object_or_404(Application, id=application_id)
#     try:
#         profile = application.candidate.candidate_profile
#         resume_text = ""
#         if profile.resume:
#             profile.resume.open()
#             resume_text = extract_text_from_resume(profile.resume)
#         if not resume_text:
#             resume_text = f"""
#             Candidate: {application.candidate.username}
#             Skills: {profile.skills}
#             Experience: {profile.experience_years} years
#             Education: {profile.education}
#             Current Position: {profile.current_position}
#             Cover Letter: {application.cover_letter}
#             """
#         result = screen_resume(
#             resume_text,
#             application.job.description,
#             application.job.skills
#         )
#         application.ai_score = result['score']
#         application.ai_feedback = f"""
# Summary: {result['summary']}
# Strengths: {result['strengths']}
# Gaps: {result['gaps']}
# Recommendation: {result['recommendation']}
#         """
#         application.save()
#         messages.success(request, f'AI screening complete! Score: {result["score"]}%')
#         return render(request, 'ai_engine/screening_result.html', {
#             'application': application,
#             'result': result
#         })
#     except Exception as e:
#         messages.error(request, f'AI screening failed: {str(e)}')
#         return redirect('jobs:dashboard')

# @login_required
# def generate_jd(request):
#     if not request.user.is_employer():
#         return redirect('jobs:list')
#     if request.method == 'POST':
#         title = request.POST.get('title', '')
#         skills = request.POST.get('skills', '')
#         experience = request.POST.get('experience', '')
#         job_type = request.POST.get('job_type', '')
#         location = request.POST.get('location', '')
#         try:
#             generated_text = generate_job_description(
#                 title, skills, experience, job_type, location
#             )
#             return render(request, 'ai_engine/generate_jd.html', {
#                 'generated': generated_text,
#                 'form_data': request.POST
#             })
#         except Exception as e:
#             messages.error(request, f'Failed to generate JD: {str(e)}')
#     return render(request, 'ai_engine/generate_jd.html', {})

# @login_required
# def skill_match(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     try:
#         profile = request.user.candidate_profile
#         result = match_skills(profile.skills, job.skills)
#         return render(request, 'ai_engine/skill_match.html', {
#             'job': job,
#             'result': result,
#             'profile': profile
#         })
#     except CandidateProfile.DoesNotExist:
#         messages.warning(request, 'Please complete your profile first.')
#         return redirect('candidates:edit_profile')




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from jobs.models import Job, Application
from candidates.models import CandidateProfile
from .utils import screen_resume, generate_job_description, match_skills
import PyPDF2
import io


def extract_text_from_resume(resume_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() or ''
        return text.strip()
    except Exception:
        return ''


def get_employer_plan(user):
    """Returns the employer's active subscription plan or None."""
    try:
        sub = user.subscription
        if sub.is_active() and sub.plan:
            return sub.plan
    except Exception:
        pass
    return None


@login_required
def screen_application(request, application_id):
    if not request.user.is_employer():
        messages.error(request, 'Employers only.')
        return redirect('jobs:list')

    application = get_object_or_404(Application, id=application_id)

    # ── FIX 2: Check if employer's plan allows AI screening ──
    plan = get_employer_plan(request.user)
    if not plan or not plan.ai_screening:
        messages.error(
            request,
            'AI screening is not available on your current plan. '
            'Please upgrade to Starter or Pro to use this feature.'
        )
        return redirect('payments:pricing')
    # ── END FIX 2 ──

    try:
        profile = application.candidate.candidate_profile
        resume_text = ''
        if profile.resume:
            profile.resume.open()
            resume_text = extract_text_from_resume(profile.resume)

        # Fallback: build text from profile fields if PDF extraction failed
        if not resume_text:
            resume_text = (
                f"Candidate: {application.candidate.username}\n"
                f"Skills: {profile.skills}\n"
                f"Experience: {profile.experience_years} years\n"
                f"Education: {profile.education}\n"
                f"Current Position: {profile.current_position}\n"
                f"Cover Letter: {application.cover_letter}"
            )

        result = screen_resume(
            resume_text,
            application.job.description,
            application.job.skills
        )

        application.ai_score = result['score']
        application.ai_feedback = (
            f"Summary: {result['summary']}\n"
            f"Strengths: {result['strengths']}\n"
            f"Gaps: {result['gaps']}\n"
            f"Recommendation: {result['recommendation']}"
        )
        application.save()

        messages.success(request, f'AI screening complete! Score: {result["score"]}%')
        return render(request, 'ai_engine/screening_result.html', {
            'application': application,
            'result': result
        })

    except Exception as e:
        messages.error(request, f'AI screening failed: {str(e)}')
        return redirect('jobs:dashboard')


@login_required
def generate_jd(request):
    if not request.user.is_employer():
        return redirect('jobs:list')
    if request.method == 'POST':
        title = request.POST.get('title', '')
        skills = request.POST.get('skills', '')
        experience = request.POST.get('experience', '')
        job_type = request.POST.get('job_type', '')
        location = request.POST.get('location', '')
        try:
            generated_text = generate_job_description(
                title, skills, experience, job_type, location
            )
            return render(request, 'ai_engine/generate_jd.html', {
                'generated': generated_text,
                'form_data': request.POST
            })
        except Exception as e:
            messages.error(request, f'Failed to generate JD: {str(e)}')
    return render(request, 'ai_engine/generate_jd.html', {})


@login_required
def skill_match(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    try:
        profile = request.user.candidate_profile
        result = match_skills(profile.skills, job.skills)
        return render(request, 'ai_engine/skill_match.html', {
            'job': job,
            'result': result,
            'profile': profile
        })
    except CandidateProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile first.')
        return redirect('candidates:edit_profile')