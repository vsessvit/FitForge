from django.db import models


class ProductCategory(models.Model):
    """Model for product categories (Apparel, Equipment, Supplements)"""
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Product Categories'
    
    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
