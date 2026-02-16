from django.db import models
from django.contrib.auth.models import User


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
    stripe_price_id = models.CharField(max_length=255, blank=True, help_text='Stripe Price ID for subscriptions')
    stripe_product_id = models.CharField(max_length=255, blank=True, help_text='Stripe Product ID')
    
    class Meta:
        verbose_name_plural = 'Membership Tiers'
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_display()}"


class UserMembership(models.Model):
    """Model for individual user memberships"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    membership_tier = models.ForeignKey('MembershipTier', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    auto_renew = models.BooleanField(default=False)
    classes_used_this_week = models.IntegerField(default=0)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, help_text='Stripe Subscription ID')
    stripe_customer_id = models.CharField(max_length=255, blank=True, help_text='Stripe Customer ID')
    
    class Meta:
        verbose_name_plural = 'User Memberships'
    
    def __str__(self):
        return f"{self.user.username} - {self.membership_tier.name if self.membership_tier else 'No Tier'}"
