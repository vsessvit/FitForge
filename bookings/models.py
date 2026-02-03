from django.db import models
from django.contrib.auth.models import User
from classes.models import ClassSchedule


class Booking(models.Model):
    """Model for class bookings"""
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Bookings'
        unique_together = ['user', 'class_schedule']
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.class_schedule}"
