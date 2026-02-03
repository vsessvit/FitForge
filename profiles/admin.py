from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth', 'emergency_contact_name')
    search_fields = ('user__username', 'user__email', 'phone_number', 'emergency_contact_name')
    list_filter = ('date_of_birth',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'date_of_birth')
        }),
        ('Fitness Information', {
            'fields': ('fitness_goals',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
    )
