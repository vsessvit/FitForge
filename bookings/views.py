from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from classes.models import ClassSchedule
from memberships.models import UserMembership
from .models import Booking
from .forms import BookingForm


@login_required
def create_booking(request, schedule_id):
    """View to create a new booking for a class"""
    schedule = get_object_or_404(ClassSchedule, pk=schedule_id)
    
    # Check if user has an active membership
    try:
        user_membership = UserMembership.objects.get(user=request.user, is_active=True)
    except UserMembership.DoesNotExist:
        messages.error(request, 'You need an active membership to book classes. Please purchase a membership first.')
        return redirect('memberships:membership_plans')
    
    # Check if schedule not full
    if schedule.available_spots <= 0:
        messages.error(request, 'Sorry, this class is full. Please choose another time.')
        return redirect('class_schedule_list')
    
    # Check if schedule is active
    if not schedule.is_active:
        messages.error(request, 'This class schedule is no longer active.')
        return redirect('class_schedule_list')
    
    # Check for duplicate booking
    existing_booking = Booking.objects.filter(
        user=request.user,
        class_schedule=schedule,
        status__in=['confirmed', 'attended']
    ).exists()
    
    if existing_booking:
        messages.warning(request, 'You have already booked this class.')
        return redirect('bookings:my_bookings')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user, schedule=schedule)
        if form.is_valid():
            # Use transaction to ensure data consistency
            with transaction.atomic():
                # Create booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.class_schedule = schedule
                booking.status = 'confirmed'
                booking.save()
                
                # Decrease available spots
                schedule.available_spots -= 1
                schedule.save()
            
            messages.success(request, f'Successfully booked {schedule.fitness_class.name} on {schedule.date}!')
            return redirect('bookings:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm(user=request.user, schedule=schedule)
    
    context = {
        'form': form,
        'schedule': schedule,
    }
    
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_confirmation(request, booking_id):
    """View to display booking confirmation"""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/booking_confirmation.html', context)


@login_required
def my_bookings(request):
    """View to display user's bookings"""
    now = timezone.now()
    
    # Get upcoming bookings (future dates, confirmed or attended status)
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        class_schedule__date__gte=now.date(),
        status__in=['confirmed', 'attended']
    ).select_related('class_schedule', 'class_schedule__fitness_class').order_by('class_schedule__date', 'class_schedule__start_time')
    
    # Get past bookings
    past_bookings = Booking.objects.filter(
        user=request.user,
        class_schedule__date__lt=now.date()
    ).select_related('class_schedule', 'class_schedule__fitness_class').order_by('-class_schedule__date', '-class_schedule__start_time')
    
    # Get cancelled bookings
    cancelled_bookings = Booking.objects.filter(
        user=request.user,
        status='cancelled'
    ).select_related('class_schedule', 'class_schedule__fitness_class').order_by('-class_schedule__date', '-class_schedule__start_time')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'cancelled_bookings': cancelled_bookings,
        'now': now,
    }
    
    return render(request, 'bookings/my_bookings.html', context)


@login_required
def cancel_booking(request, booking_id):
    """View to cancel a booking"""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    # Check if booking can be cancelled (must be confirmed and in the future)
    now = timezone.now()
    if booking.class_schedule.date < now.date():
        messages.error(request, 'Cannot cancel a past booking.')
        return redirect('bookings:my_bookings')
    
    if booking.status == 'cancelled':
        messages.warning(request, 'This booking is already cancelled.')
        return redirect('bookings:my_bookings')
    
    if request.method == 'POST':
        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Update booking status
            booking.status = 'cancelled'
            booking.save()
            
            # Restore available spot
            schedule = booking.class_schedule
            schedule.available_spots += 1
            schedule.save()
        
        messages.success(request, f'Your booking for {booking.class_schedule.fitness_class.name} on {booking.class_schedule.date} has been cancelled.')
        return redirect('bookings:my_bookings')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/cancel_booking.html', context)

