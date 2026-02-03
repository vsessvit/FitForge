from django.db import models


class MembershipTier(models.Model):
    """Model for membership plan tiers (Basic, Premium, Elite)"""
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='monthly')
    classes_per_week = models.IntegerField(help_text='Number of classes allowed per week')
    has_personal_training = models.BooleanField(default=False)
    has_nutrition_plan = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Membership Tiers'
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_display()}"
