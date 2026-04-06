from django import forms
from .models import Job, Company, Application

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'website', 'description', 'location')

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'requirements', 'skills',
                  'job_type', 'experience', 'salary_min', 'salary_max',
                  'location', 'deadline')

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('cover_letter',)
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Why are you a good fit for this role?'})
        }