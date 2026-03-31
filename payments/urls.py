from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.pricing, name='pricing'),
    path('checkout/<str:plan_name>/', views.create_checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('billing/', views.billing_dashboard, name='billing'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]