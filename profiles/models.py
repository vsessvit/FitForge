from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User profile for storing additional user information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    fitness_goals = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
