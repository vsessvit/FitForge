from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, ProductCategory


def all_products(request):
    """Display all products with optional category filtering, search, and sorting"""
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    current_category = None
    search_query = None
    sort = None
    direction = None
    
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
    
    # Sorting functionality
    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        
        # Handle combined sort&direction parameters (e.g., "price&direction=desc")
        if '&' in sortkey:
            parts = sortkey.split('&')
            sortkey = parts[0]
            if len(parts) > 1 and 'direction=' in parts[1]:
                direction = parts[1].split('=')[1]
        
        sort = sortkey
        
        # Check for separate direction parameter
        if 'direction' in request.GET and not direction:
            direction = request.GET['direction']
        
        # Apply sorting
        if sortkey == 'price':
            sortkey = 'price'
        elif sortkey == 'rating':
            sortkey = '-rating'  # Default to high to low for popularity
            if direction and direction == 'asc':
                sortkey = 'rating'
        
        if sortkey != 'rating' and direction == 'desc':
            sortkey = f'-{sortkey}'
        
        products = products.order_by(sortkey)
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """Display a single product's details"""
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
