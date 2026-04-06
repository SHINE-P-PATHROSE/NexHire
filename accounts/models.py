from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    )
<<<<<<< HEAD
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
=======
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Job Seeker')
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_employer(self):
        return self.role == 'employer'

    def is_candidate(self):
<<<<<<< HEAD
        return self.role == 'candidate'
=======
        return self.role == 'candidate'
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
