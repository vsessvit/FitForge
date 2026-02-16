from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    Display the user's profile
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's upcoming bookings
    from bookings.models import Booking
    now = timezone.now()
    bookings = Booking.objects.filter(
        user=request.user,
        class_schedule__date__gte=now.date(),
        status='confirmed'
    ).select_related('class_schedule', 'class_schedule__fitness_class').order_by('class_schedule__date', 'class_schedule__start_time')[:5]
    
    upcoming_count = bookings.count()
    
    # Get user's active membership
    from memberships.models import UserMembership
    try:
        active_membership = UserMembership.objects.filter(
            user=request.user,
            is_active=True,
            status='active'
        ).select_related('tier').first()
    except UserMembership.DoesNotExist:
        active_membership = None
    
    context = {
        'profile': profile,
        'form': form,
        'bookings': bookings,
        'upcoming_count': upcoming_count,
        'active_membership': active_membership,
    }
    
    return render(request, 'profiles/profile.html', context)
