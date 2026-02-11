from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from classes.models import ClassSchedule


class BookingForm(forms.ModelForm):
    """Form for creating a booking"""
    
    class Meta:
        model = Booking
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Any special notes or requirements? (Optional)',
                'class': 'form-control'
            }),
        }
        labels = {
            'notes': 'Additional Notes',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.schedule = kwargs.pop('schedule', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate user is provided
        if not self.user:
            raise ValidationError('User must be logged in to book a class.')
        
        # Validate schedule is provided
        if not self.schedule:
            raise ValidationError('Class schedule must be specified.')
        
        # Check if schedule is still active
        if not self.schedule.is_active:
            raise ValidationError('This class schedule is no longer active.')
        
        # Check if there are available spots
        if self.schedule.available_spots <= 0:
            raise ValidationError('Sorry, this class is full. No spots available.')
        
        # Check for duplicate booking
        existing_booking = Booking.objects.filter(
            user=self.user,
            class_schedule=self.schedule,
            status__in=['confirmed', 'attended']
        ).exists()
        
        if existing_booking:
            raise ValidationError('You have already booked this class.')
        
        return cleaned_data
