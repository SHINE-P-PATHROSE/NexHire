from django.db import models
from accounts.models import User

class CandidateProfile(models.Model):
    AVAILABILITY_CHOICES = (
        ('immediate', 'Immediate'),
        ('2_weeks', '2 Weeks Notice'),
        ('1_month', '1 Month Notice'),
        ('not_looking', 'Not Looking'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True, help_text='Comma separated e.g. Python, Django')
    experience_years = models.IntegerField(default=0)
    education = models.CharField(max_length=300, blank=True)
    current_position = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='immediate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]