from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Booking


@receiver(post_save, sender=Booking)
def update_booking_status(sender, instance, created, **kwargs):
    """
    Signal to handle booking status changes
    Note: Available spots are managed in views with transactions for data integrity
    This signal can be used for notifications, logging, or other side effects
    """
    if created:
        # Log new booking creation or send notifications
        pass
    else:
        # Handle status changes (e.g., send cancellation emails)
        if instance.status == 'cancelled':
            # Could send cancellation confirmation email here
            pass
