from django.shortcuts import render
from .models import Product, ProductCategory


def all_products(request):
    """Display all products with optional category filtering"""
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    current_category = None
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)
        current_category = ProductCategory.objects.filter(name=category).first()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    }
    
    return render(request, 'products/all_products.html', context)
