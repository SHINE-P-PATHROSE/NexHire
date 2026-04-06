<<<<<<< HEAD
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.conf import settings
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Plan, Subscription, Payment
# import stripe
# import json

# stripe.api_key = settings.STRIPE_SECRET_KEY

# PLAN_PRICES = {
#     'starter': 99900,   # ₹999 in paise
#     'pro': 299900,      # ₹2999 in paise
# }

# def pricing(request):
#     plans = Plan.objects.all()
#     user_plan = None
#     if request.user.is_authenticated:
#         try:
#             user_plan = request.user.subscription.plan.name
#         except:
#             user_plan = 'free'
#     return render(request, 'payments/pricing.html', {
#         'plans': plans,
#         'user_plan': user_plan,
#         'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
#     })

# @login_required
# def create_checkout(request, plan_name):
#     if not request.user.is_employer():
#         messages.error(request, 'Only employers can subscribe.')
#         return redirect('payments:pricing')
#     if plan_name not in PLAN_PRICES:
#         messages.error(request, 'Invalid plan.')
#         return redirect('payments:pricing')
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'inr',
#                     'unit_amount': PLAN_PRICES[plan_name],
#                     'product_data': {
#                         'name': f'AI Job Board - {plan_name.title()} Plan',
#                         'description': f'Monthly subscription for {plan_name} plan',
#                     },
#                     'recurring': {'interval': 'month'},
#                 },
#                 'quantity': 1,
#             }],
#             mode='subscription',
#             success_url=request.build_absolute_uri('/payments/success/') + '?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url=request.build_absolute_uri('/payments/cancel/'),
#             metadata={
#                 'user_id': request.user.id,
#                 'plan_name': plan_name,
#             }
#         )
#         return redirect(checkout_session.url)
#     except Exception as e:
#         messages.error(request, f'Payment failed: {str(e)}')
#         return redirect('payments:pricing')

# @login_required
# def payment_success(request):
#     session_id = request.GET.get('session_id')
#     if session_id:
#         try:
#             session = stripe.checkout.Session.retrieve(session_id)
#             plan_name = session.metadata.get('plan_name')
#             plan = Plan.objects.get(name=plan_name)
#             subscription, created = Subscription.objects.get_or_create(
#                 employer=request.user,
#                 defaults={'plan': plan, 'status': 'active'}
#             )
#             if not created:
#                 subscription.plan = plan
#                 subscription.status = 'active'
#                 subscription.stripe_subscription_id = session.subscription
#                 subscription.stripe_customer_id = session.customer
#                 subscription.save()
#             Payment.objects.create(
#                 employer=request.user,
#                 plan=plan,
#                 stripe_payment_id=session.payment_intent or session_id,
#                 amount=PLAN_PRICES[plan_name] // 100,
#                 status='paid'
#             )
#             messages.success(request, f'Successfully subscribed to {plan_name.title()} plan!')
#         except Exception as e:
#             messages.error(request, f'Error processing payment: {str(e)}')
#     return render(request, 'payments/success.html')

# @login_required
# def payment_cancel(request):
#     messages.warning(request, 'Payment cancelled.')
#     return render(request, 'payments/cancel.html')

# @login_required
# def billing_dashboard(request):
#     try:
#         subscription = request.user.subscription
#     except:
#         subscription = None
#     payments = Payment.objects.filter(employer=request.user).order_by('-created_at')
#     return render(request, 'payments/billing.html', {
#         'subscription': subscription,
#         'payments': payments
#     })

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#         if event['type'] == 'customer.subscription.deleted':
#             subscription_id = event['data']['object']['id']
#             try:
#                 sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
#                 sub.status = 'cancelled'
#                 sub.save()
#             except Subscription.DoesNotExist:
#                 pass
#         return HttpResponse(status=200)
#     except Exception as e:
#         return HttpResponse(status=400)


=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plan, Subscription, Payment
<<<<<<< HEAD
from accounts.models import User
=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

PLAN_PRICES = {
    'starter': 99900,   # ₹999 in paise
    'pro': 299900,      # ₹2999 in paise
}

<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
def pricing(request):
    plans = Plan.objects.all()
    user_plan = None
    if request.user.is_authenticated:
        try:
            user_plan = request.user.subscription.plan.name
<<<<<<< HEAD
        except Exception:
=======
        except:
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
            user_plan = 'free'
    return render(request, 'payments/pricing.html', {
        'plans': plans,
        'user_plan': user_plan,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY
    })

<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
@login_required
def create_checkout(request, plan_name):
    if not request.user.is_employer():
        messages.error(request, 'Only employers can subscribe.')
        return redirect('payments:pricing')
    if plan_name not in PLAN_PRICES:
        messages.error(request, 'Invalid plan.')
        return redirect('payments:pricing')
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': PLAN_PRICES[plan_name],
                    'product_data': {
<<<<<<< HEAD
                        'name': f'NexHire - {plan_name.title()} Plan',
=======
                        'name': f'AI Job Board - {plan_name.title()} Plan',
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
                        'description': f'Monthly subscription for {plan_name} plan',
                    },
                    'recurring': {'interval': 'month'},
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/payments/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
            metadata={
                'user_id': request.user.id,
                'plan_name': plan_name,
            }
        )
        return redirect(checkout_session.url)
    except Exception as e:
        messages.error(request, f'Payment failed: {str(e)}')
        return redirect('payments:pricing')

<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            plan_name = session.metadata.get('plan_name')
            plan = Plan.objects.get(name=plan_name)
            subscription, created = Subscription.objects.get_or_create(
                employer=request.user,
<<<<<<< HEAD
                defaults={
                    'plan': plan,
                    'status': 'active',
                    'stripe_subscription_id': session.subscription,
                    'stripe_customer_id': session.customer,
                }
=======
                defaults={'plan': plan, 'status': 'active'}
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
            )
            if not created:
                subscription.plan = plan
                subscription.status = 'active'
                subscription.stripe_subscription_id = session.subscription
                subscription.stripe_customer_id = session.customer
                subscription.save()
            Payment.objects.create(
                employer=request.user,
                plan=plan,
                stripe_payment_id=session.payment_intent or session_id,
                amount=PLAN_PRICES[plan_name] // 100,
                status='paid'
            )
            messages.success(request, f'Successfully subscribed to {plan_name.title()} plan!')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
    return render(request, 'payments/success.html')

<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
@login_required
def payment_cancel(request):
    messages.warning(request, 'Payment cancelled.')
    return render(request, 'payments/cancel.html')

<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
@login_required
def billing_dashboard(request):
    try:
        subscription = request.user.subscription
<<<<<<< HEAD
    except Exception:
=======
    except:
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
        subscription = None
    payments = Payment.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'payments/billing.html', {
        'subscription': subscription,
        'payments': payments
    })

<<<<<<< HEAD

# ── FIX 7: Webhook handles checkout.session.completed + invoice.paid + subscription.deleted ──
=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
<<<<<<< HEAD

=======
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
<<<<<<< HEAD
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event['type']
    data = event['data']['object']

    # ── New subscription created via Checkout ──
    if event_type == 'checkout.session.completed':
        _handle_checkout_completed(data)

    # ── Recurring invoice paid (monthly renewal) ──
    elif event_type == 'invoice.paid':
        _handle_invoice_paid(data)

    # ── Subscription cancelled (from Stripe dashboard or customer portal) ──
    elif event_type == 'customer.subscription.deleted':
        _handle_subscription_deleted(data)

    # ── Subscription renewed / updated ──
    elif event_type == 'customer.subscription.updated':
        _handle_subscription_updated(data)

    return HttpResponse(status=200)


def _handle_checkout_completed(session):
    """Activate subscription when checkout is completed via webhook (reliable fallback)."""
    try:
        user_id = session.get('metadata', {}).get('user_id')
        plan_name = session.get('metadata', {}).get('plan_name')
        if not user_id or not plan_name:
            return
        user = User.objects.get(id=user_id)
        plan = Plan.objects.get(name=plan_name)
        subscription, created = Subscription.objects.get_or_create(
            employer=user,
            defaults={
                'plan': plan,
                'status': 'active',
                'stripe_subscription_id': session.get('subscription'),
                'stripe_customer_id': session.get('customer'),
            }
        )
        if not created:
            subscription.plan = plan
            subscription.status = 'active'
            subscription.stripe_subscription_id = session.get('subscription')
            subscription.stripe_customer_id = session.get('customer')
            subscription.save()
    except Exception:
        pass


def _handle_invoice_paid(invoice):
    """Keep subscription active on each successful renewal payment."""
    try:
        stripe_subscription_id = invoice.get('subscription')
        if not stripe_subscription_id:
            return
        sub = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
        sub.status = 'active'
        sub.save()

        # Record the renewal payment
        amount_paid = invoice.get('amount_paid', 0) // 100  # paise → rupees
        Payment.objects.create(
            employer=sub.employer,
            plan=sub.plan,
            stripe_payment_id=invoice.get('payment_intent', invoice.get('id', '')),
            amount=amount_paid,
            currency=invoice.get('currency', 'inr'),
            status='paid'
        )
    except Subscription.DoesNotExist:
        pass
    except Exception:
        pass


def _handle_subscription_deleted(stripe_sub):
    """Mark subscription as cancelled when deleted in Stripe."""
    try:
        sub = Subscription.objects.get(stripe_subscription_id=stripe_sub.get('id'))
        sub.status = 'cancelled'
        sub.save()
    except Subscription.DoesNotExist:
        pass


def _handle_subscription_updated(stripe_sub):
    """Sync subscription status when updated in Stripe (e.g. plan upgrade from portal)."""
    try:
        sub = Subscription.objects.get(stripe_subscription_id=stripe_sub.get('id'))
        stripe_status = stripe_sub.get('status')
        # Map Stripe statuses to our statuses
        status_map = {
            'active': 'active',
            'canceled': 'cancelled',
            'past_due': 'expired',
            'unpaid': 'expired',
            'incomplete_expired': 'expired',
        }
        sub.status = status_map.get(stripe_status, 'expired')
        sub.save()
    except Subscription.DoesNotExist:
        pass
=======
        if event['type'] == 'customer.subscription.deleted':
            subscription_id = event['data']['object']['id']
            try:
                sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
                sub.status = 'cancelled'
                sub.save()
            except Subscription.DoesNotExist:
                pass
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
>>>>>>> 0d4f6ab7783f4a2327d527d34e1508069705d978
