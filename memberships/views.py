from django.shortcuts import render, get_object_or_404
from .models import MembershipTier


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
