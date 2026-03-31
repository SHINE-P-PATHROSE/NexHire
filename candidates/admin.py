from django.contrib import admin
from .models import CandidateProfile

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_position', 'experience_years', 'location', 'availability')
    search_fields = ('user__username', 'skills')
    list_filter = ('availability',)