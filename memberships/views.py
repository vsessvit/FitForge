from django.shortcuts import render
from .models import MembershipTier


def membership_plans(request):
    """Display all available membership plans"""
    plans = MembershipTier.objects.filter(is_active=True).order_by('price')
    
    context = {
        'plans': plans,
    }
    
    return render(request, 'memberships/membership_plans.html', context)
