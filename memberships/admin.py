from django.contrib import admin
from .models import MembershipTier, UserMembership


@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'classes_per_week', 'is_active')
    list_filter = ('duration', 'is_active')
    search_fields = ('name',)


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_tier', 'start_date', 'end_date', 'status', 'auto_renew')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'start_date'
