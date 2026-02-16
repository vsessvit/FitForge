from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import MembershipTier, UserMembership
import stripe

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
