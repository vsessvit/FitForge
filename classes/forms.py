from django import forms
from classes.models import ClassSchedule, FitnessClass
from datetime import datetime, timedelta


class ScheduleCreationForm(forms.ModelForm):
    """Form for admins to create class schedules"""
    
    class Meta:
        model = ClassSchedule
        fields = ['fitness_class', 'date', 'start_time', 'end_time', 'available_spots', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'available_spots': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fitness_class': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set available spots to class max capacity by default
        if 'fitness_class' in self.data:
            try:
                fitness_class_id = int(self.data.get('fitness_class'))
                fitness_class = FitnessClass.objects.get(id=fitness_class_id)
                self.fields['available_spots'].initial = fitness_class.max_capacity
            except (ValueError, TypeError, FitnessClass.DoesNotExist):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError('End time must be after start time.')
        
        return cleaned_data


class BulkScheduleCreationForm(forms.Form):
    """Form for creating recurring class schedules"""
    
    fitness_class = forms.ModelChoiceField(
        queryset=FitnessClass.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Class'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Date'
    )
    days_of_week = forms.MultipleChoiceField(
        choices=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Days of Week'
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Class Start Time'
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Class End Time'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError('End date must be after start date.')
            
            # Limit to 3 months to prevent accidental huge bulk creates
            if (end_date - start_date).days > 90:
                raise forms.ValidationError('Bulk creation limited to 3 months maximum.')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError('End time must be after start time.')
        
        return cleaned_data
