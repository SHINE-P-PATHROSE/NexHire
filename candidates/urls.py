from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('dashboard/', views.candidate_dashboard, name='dashboard'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('applications/', views.my_applications, name='my_applications'),
]