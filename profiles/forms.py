from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile information"""
    
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'fitness_goals': 'Your Fitness Goals',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_phone': 'Emergency Contact Phone',
        }

        for field in self.fields:
            if field != 'date_of_birth':
                placeholder = placeholders.get(field, '')
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = placeholders.get(field, field.replace('_', ' ').title())
