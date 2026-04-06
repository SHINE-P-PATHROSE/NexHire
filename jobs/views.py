# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Job, Company, Application
# from .forms import JobForm, CompanyForm, ApplicationForm

# def job_list(request):
#     jobs = Job.objects.filter(status='active').order_by('-created_at')
#     search = request.GET.get('search', '')
#     job_type = request.GET.get('job_type', '')
#     experience = request.GET.get('experience', '')
#     if search:
#         from django.db.models import Q
#         jobs = jobs.filter(Q(title__icontains=search) | Q(skills__icontains=search) | Q(description__icontains=search))
#     if job_type:
#         jobs = jobs.filter(job_type=job_type)
#     if experience:
#         jobs = jobs.filter(experience=experience)
#     return render(request, 'jobs/job_list.html', {'jobs': jobs})

# def job_detail(request, pk):
#     job = get_object_or_404(Job, pk=pk)
#     already_applied = False
#     if request.user.is_authenticated:
#         already_applied = Application.objects.filter(job=job, candidate=request.user).exists()
#     return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})

# @login_required
# def employer_dashboard(request):
#     if not request.user.is_employer():
#         messages.error(request, 'Access denied. Employers only.')
#         return redirect('jobs:list')
#     try:
#         company = request.user.company
#         jobs = company.jobs.all().order_by('-created_at')
#     except Company.DoesNotExist:
#         company = None
#         jobs = []
#     return render(request, 'jobs/employer_dashboard.html', {'company': company, 'jobs': jobs})

# @login_required
# def create_job(request):
#     if not request.user.is_employer():
#         return redirect('jobs:list')
#     try:
#         company = request.user.company
#     except Company.DoesNotExist:
#         messages.warning(request, 'Please create your company profile first.')
#         return redirect('jobs:create_company')
#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.company = company
#             job.save()
#             messages.success(request, 'Job posted successfully!')
#             return redirect('jobs:dashboard')
#     else:
#         form = JobForm()
#     return render(request, 'jobs/create_job.html', {'form': form})

# @login_required
# def create_company(request):
#     if request.method == 'POST':
#         form = CompanyForm(request.POST, request.FILES)
#         if form.is_valid():
#             company = form.save(commit=False)
#             company.owner = request.user
#             company.save()
#             messages.success(request, 'Company profile created!')
#             return redirect('jobs:dashboard')
#     else:
#         form = CompanyForm()
#     return render(request, 'jobs/create_company.html', {'form': form})

# @login_required
# def apply_job(request, pk):
#     job = get_object_or_404(Job, pk=pk)
#     if request.user.is_employer():
#         messages.error(request, 'Employers cannot apply for jobs.')
#         return redirect('jobs:detail', pk=pk)
#     if Application.objects.filter(job=job, candidate=request.user).exists():
#         messages.warning(request, 'You have already applied for this job.')
#         return redirect('jobs:detail', pk=pk)
#     if request.method == 'POST':
#         form = ApplicationForm(request.POST)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.candidate = request.user
#             application.save()
#             messages.success(request, 'Application submitted successfully!')
#             return redirect('candidates:dashboard')
#     else:
#         form = ApplicationForm()
#     return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

# -------------------------------------------------------------------------------------------------------




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Company, Application
from .forms import JobForm, CompanyForm, ApplicationForm


def get_employer_plan(user):
    """Returns the employer's active subscription plan, or None if on free/no plan."""
    try:
        sub = user.subscription
        if sub.is_active() and sub.plan:
            return sub.plan
    except Exception:
        pass
    return None


def job_list(request):
    jobs = Job.objects.filter(status='active').order_by('-created_at')
    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    experience = request.GET.get('experience', '')
    if search:
        from django.db.models import Q
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(skills__icontains=search) |
            Q(description__icontains=search)
        )
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if experience:
        jobs = jobs.filter(experience=experience)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})


@login_required
def employer_dashboard(request):
    if not request.user.is_employer():
        messages.error(request, 'Access denied. Employers only.')
        return redirect('jobs:list')
    try:
        company = request.user.company
        jobs = company.jobs.all().order_by('-created_at')
    except Company.DoesNotExist:
        company = None
        jobs = []
    return render(request, 'jobs/employer_dashboard.html', {'company': company, 'jobs': jobs})


@login_required
def create_job(request):
    if not request.user.is_employer():
        return redirect('jobs:list')

    try:
        company = request.user.company
    except Company.DoesNotExist:
        messages.warning(request, 'Please create your company profile first.')
        return redirect('jobs:create_company')

    # ── FIX 1: Enforce job_post_limit based on active subscription plan ──
    plan = get_employer_plan(request.user)
    if plan:
        job_limit = plan.job_post_limit
    else:
        # No active subscription → treat as free plan (limit = 1)
        from payments.models import Plan
        try:
            free_plan = Plan.objects.get(name='free')
            job_limit = free_plan.job_post_limit
        except Plan.DoesNotExist:
            job_limit = 1  # hard fallback

    current_job_count = company.jobs.filter(status__in=['active', 'draft']).count()

    if current_job_count >= job_limit:
        messages.error(
            request,
            f'You have reached your plan limit of {job_limit} job posting(s). '
            f'Please upgrade your plan to post more jobs.'
        )
        return redirect('payments:pricing')
    # ── END FIX 1 ──

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {
        'form': form,
        'job_limit': job_limit,
        'current_job_count': current_job_count,
    })


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, 'Company profile created!')
            return redirect('jobs:dashboard')
    else:
        form = CompanyForm()
    return render(request, 'jobs/create_company.html', {'form': form})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user.is_employer():
        messages.error(request, 'Employers cannot apply for jobs.')
        return redirect('jobs:detail', pk=pk)
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('candidates:dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})