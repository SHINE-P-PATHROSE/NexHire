from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CandidateProfile
from .forms import CandidateProfileForm
from jobs.models import Application

@login_required
def candidate_dashboard(request):
    if request.user.is_employer():
        return redirect('jobs:dashboard')
    # Auto create profile if doesn't exist
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(
        candidate=request.user
    ).select_related('job', 'job__company').order_by('-applied_at')
    return render(request, 'candidates/dashboard.html', {
        'profile': profile,
        'applications': applications,
        'total_applications': applications.count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'rejected': applications.filter(status='rejected').count(),
    })

@login_required
def edit_profile(request):
    if request.user.is_employer():
        return redirect('jobs:dashboard')
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('candidates:dashboard')
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, 'candidates/edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    return render(request, 'candidates/view_profile.html', {'profile': profile})

@login_required
def my_applications(request):
    applications = Application.objects.filter(
        candidate=request.user
    ).select_related('job', 'job__company').order_by('-applied_at')
    return render(request, 'candidates/my_applications.html', {
        'applications': applications
    })