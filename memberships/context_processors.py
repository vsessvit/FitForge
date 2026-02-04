from .models import UserMembership


def user_membership(request):
    """Context processor to make user's membership available in all templates"""
    context = {}
    
    if request.user.is_authenticated:
        try:
            membership = UserMembership.objects.select_related('membership_tier').get(
                user=request.user,
                status='active'
            )
            context['user_membership'] = membership
        except UserMembership.DoesNotExist:
            context['user_membership'] = None
    else:
        context['user_membership'] = None
    
    return context
