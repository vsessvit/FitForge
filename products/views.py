from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, ProductCategory
from .forms import ProductForm


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
            if direction == 'desc':
                sortkey = '-price'
            else:
                sortkey = 'price'
        elif sortkey == 'rating':
            if direction == 'desc':
                sortkey = '-rating'
            else:
                sortkey = 'rating'
        
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


@login_required
def add_product(request):
    """Add a product to the store (admin only)"""
    # Check if user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully added product: {product.name}')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit a product in the store (admin only)"""
    # Check if user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated product: {product.name}')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store (admin only)"""
    # Check if user is a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Product "{product.name}" has been deleted.')
    return redirect(reverse('products:all_products'))
