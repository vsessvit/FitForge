from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_schedule', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'user__email', 'class_schedule__fitness_class__name')
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_date',)
