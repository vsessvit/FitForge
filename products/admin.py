from django.contrib import admin
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'stock_quantity', 'rating')
    list_filter = ('category', 'rating')
    search_fields = ('name', 'sku', 'description')
    ordering = ('name',)
