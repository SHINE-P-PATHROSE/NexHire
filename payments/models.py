from django.db import models
from accounts.models import User

class Plan(models.Model):
    PLAN_CHOICES = (
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('pro', 'Pro'),
    )
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.IntegerField(default=0, help_text='Price in INR')
    job_post_limit = models.IntegerField(default=1)
    ai_screening = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}/month"

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )
    employer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    stripe_subscription_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employer.username} - {self.plan.name}"

    def is_active(self):
        return self.status == 'active'

class Payment(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    stripe_payment_id = models.CharField(max_length=200)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='inr')
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employer.username} - ₹{self.amount} - {self.status}"