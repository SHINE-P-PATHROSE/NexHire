from django import forms
from .models import CandidateProfile

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = (
            'bio', 'skills', 'experience_years', 'education',
            'current_position', 'location', 'linkedin',
            'github', 'availability', 'resume'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell employers about yourself...'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Python, Django, React, PostgreSQL...'}),
            'education': forms.TextInput(attrs={'placeholder': 'B.Tech Computer Science, XYZ University'}),
            'current_position': forms.TextInput(attrs={'placeholder': 'Junior Django Developer'}),
            'location': forms.TextInput(attrs={'placeholder': 'Bangalore, India'}),
        }