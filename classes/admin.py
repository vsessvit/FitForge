from django.contrib import admin
from .models import ClassCategory, FitnessClass, ClassSchedule


@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'instructor', 'duration', 'difficulty', 'max_capacity')
    list_filter = ('category', 'difficulty')
    search_fields = ('name', 'instructor')


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('fitness_class', 'date', 'start_time', 'end_time', 'available_spots', 'is_active')
    list_filter = ('date', 'is_active')
    search_fields = ('fitness_class__name',)
    date_hierarchy = 'date'
