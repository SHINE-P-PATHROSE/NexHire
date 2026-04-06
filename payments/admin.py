from django.contrib import admin
from .models import Plan, Subscription, Payment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'job_post_limit', 'ai_screening')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('employer', 'plan', 'status', 'started_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('employer', 'plan', 'amount', 'status', 'created_at')