from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='list'),
    path('<int:pk>/', views.job_detail, name='detail'),
    path('dashboard/', views.employer_dashboard, name='dashboard'),
    path('create/', views.create_job, name='create_job'),
    path('company/create/', views.create_company, name='create_company'),
    path('<int:pk>/apply/', views.apply_job, name='apply'),
]