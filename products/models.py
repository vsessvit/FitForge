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


class Product(models.Model):
    """Model for fitness products (apparel, equipment, supplements)"""
    category = models.ForeignKey('ProductCategory', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image_url = models.URLField(max_length=1024, blank=True)
    image = models.ImageField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['name']
    
    def __str__(self):
        return self.name
