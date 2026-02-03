from django.db import models


class ClassCategory(models.Model):
    """Model for fitness class categories (e.g., Yoga, HIIT, Strength)"""
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Class Categories'
    
    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name


class FitnessClass(models.Model):
    """Model for individual fitness classes"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels'),
    ]
    
    category = models.ForeignKey('ClassCategory', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text='Duration in minutes')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='all_levels')
    instructor = models.CharField(max_length=100)
    max_capacity = models.IntegerField(default=20)
    image_url = models.URLField(max_length=1024, blank=True)
    image = models.ImageField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Fitness Classes'
    
    def __str__(self):
        return self.name
