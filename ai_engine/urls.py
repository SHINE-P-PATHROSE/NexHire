from django.urls import path
from . import views

app_name = 'ai_engine'

urlpatterns = [
    path('screen/<int:application_id>/', views.screen_application, name='screen'),
    path('generate-jd/', views.generate_jd, name='generate_jd'),
    path('skill-match/<int:job_id>/', views.skill_match, name='skill_match'),
]