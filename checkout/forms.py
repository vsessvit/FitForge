from django import forms
from django.core.exceptions import ValidationError
from .models import Order


class OrderForm(forms.ModelForm):
    """Form for checkout order details"""
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'county', 'postcode', 'country',
        )

    def __init__(self, *args, **kwargs):
        """Add placeholders and classes, remove auto-generated labels"""
        membership_only = kwargs.pop('membership_only', False)
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postal Code',
            'country': 'Country',
        }

        if membership_only:
            for field_name in [
                'phone_number',
                'street_address1',
                'street_address2',
                'town_or_city',
                'county',
                'postcode',
                'country',
            ]:
                self.fields[field_name].required = False

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

    def clean_full_name(self):
        """Validate that full name contains at least first and last name"""
        full_name = self.cleaned_data.get('full_name', '').strip()
        
        # Split by spaces and filter out empty strings
        name_parts = [part for part in full_name.split() if part]
        
        if len(name_parts) < 2:
            raise ValidationError(
                'Please enter your full name (first and last name).'
            )
        
        return full_name
