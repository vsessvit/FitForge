from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import MembershipTier, UserMembership
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


def membership_plans(request):
    """Display all available membership plans"""
    plans = MembershipTier.objects.filter(is_active=True).order_by('price')
    
    context = {
        'plans': plans,
    }
    
    return render(request, 'memberships/membership_plans.html', context)


def membership_detail(request, plan_id):
    """Display detailed information about a specific membership plan"""
    plan = get_object_or_404(MembershipTier, id=plan_id, is_active=True)
    
    context = {
        'plan': plan,
    }
    
    return render(request, 'memberships/membership_detail.html', context)


@login_required
def purchase_membership(request, plan_id):
    """Handle membership purchase with Stripe"""
    plan = get_object_or_404(MembershipTier, id=plan_id, is_active=True)
    
    # Check if user already has an active membership
    try:
        existing_membership = UserMembership.objects.get(user=request.user)
        if existing_membership.status == 'active':
            messages.warning(request, 'You already have an active membership. Please cancel it before purchasing a new one.')
            return redirect('profiles:profile')
    except UserMembership.DoesNotExist:
        pass
    
    context = {
        'plan': plan,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    
    return render(request, 'memberships/purchase_membership.html', context)


@login_required
@require_POST
def create_subscription(request):
    """Create Stripe subscription"""
    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        payment_method_id = data.get('payment_method_id')
        
        plan = get_object_or_404(MembershipTier, id=plan_id, is_active=True)
        
        # Create or retrieve Stripe customer
        customer = None
        try:
            existing_membership = UserMembership.objects.get(user=request.user)
            if existing_membership.stripe_customer_id:
                customer = stripe.Customer.retrieve(existing_membership.stripe_customer_id)
        except UserMembership.DoesNotExist:
            pass
        
        if not customer:
            customer = stripe.Customer.create(
                email=request.user.email,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
                metadata={
                    'user_id': request.user.id,
                }
            )
        else:
            # Attach payment method to customer
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer.id,
            )
            stripe.Customer.modify(
                customer.id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                }
            )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': plan.stripe_price_id}],
            expand=['latest_invoice.payment_intent'],
            metadata={
                'user_id': request.user.id,
                'plan_id': plan.id,
            }
        )
        
        return JsonResponse({
            'subscriptionId': subscription.id,
            'clientSecret': subscription.latest_invoice.payment_intent.client_secret,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def activate_membership(request, plan_id):
    """Activate membership after successful payment"""
    plan = get_object_or_404(MembershipTier, id=plan_id, is_active=True)
    
    # Calculate dates based on plan duration
    start_date = datetime.now().date()
    if plan.duration == 'monthly':
        end_date = start_date + relativedelta(months=1)
    elif plan.duration == 'quarterly':
        end_date = start_date + relativedelta(months=3)
    elif plan.duration == 'annually':
        end_date = start_date + relativedelta(years=1)
    else:
        end_date = start_date + relativedelta(months=1)
    
    # Create or update membership
    membership, created = UserMembership.objects.update_or_create(
        user=request.user,
        defaults={
            'membership_tier': plan,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'active',
            'auto_renew': True,
        }
    )
    
    messages.success(request, f'Welcome to {plan.name}! Your membership is now active.')
    return redirect('memberships:membership_confirmation', membership_id=membership.id)


@login_required
def membership_confirmation(request, membership_id):
    """Display membership confirmation"""
    membership = get_object_or_404(UserMembership, id=membership_id, user=request.user)
    
    context = {
        'membership': membership,
    }
    
    return render(request, 'memberships/membership_confirmation.html', context)


@login_required
@require_POST
def cancel_membership(request):
    """Cancel user's active membership"""
    try:
        # Get active membership
        membership = UserMembership.objects.get(
            user=request.user,
            is_active=True,
            status='active'
        )
        
        # Cancel Stripe subscription if exists
        if membership.stripe_subscription_id:
            try:
                stripe.Subscription.delete(membership.stripe_subscription_id)
            except stripe.error.StripeError as e:
                messages.error(request, f'Error canceling subscription: {str(e)}')
                return redirect('profile')
        
        # Update membership status
        membership.is_active = False
        membership.status = 'cancelled'
        membership.auto_renew = False
        membership.save()
        
        messages.success(request, 'Your membership has been cancelled successfully.')
        
    except UserMembership.DoesNotExist:
        messages.error(request, 'No active membership found.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('profile')
