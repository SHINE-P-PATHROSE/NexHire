from django.contrib import admin
from .models import Company, Job, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'experience', 'status', 'created_at')
    list_filter = ('status', 'job_type', 'experience')
    search_fields = ('title', 'skills')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'ai_score', 'applied_at')
    list_filter = ('status',)