from django.shortcuts import render
from django.db.models import Q
from .models import Product, ProductCategory


def all_products(request):
    """Display all products with optional category filtering and search"""
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    current_category = None
    search_query = None
    
    # Search functionality
    if 'q' in request.GET:
        search_query = request.GET['q']
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)
        current_category = ProductCategory.objects.filter(name=category).first()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
    }
    
    return render(request, 'products/all_products.html', context)
