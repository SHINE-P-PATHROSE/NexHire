from django.db import models
from accounts.models import User
<<<<<<< HEAD
from django.utils import timezone

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978

class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    EXPERIENCE_CHOICES = (
        ('fresher', 'Fresher'),
        ('junior', '1-2 Years'),
        ('mid', '3-5 Years'),
        ('senior', '5+ Years'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    skills = models.CharField(max_length=500, help_text='Comma separated skills e.g. Python, Django, React')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',')]

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    ai_score = models.FloatField(blank=True, null=True)
    ai_feedback = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    created_at = models.DateTimeField(default=timezone.now, editable=False)
=======

>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
    class Meta:
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.candidate.username} → {self.job.title}"