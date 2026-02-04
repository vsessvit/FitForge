from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import FitnessClass, ClassCategory


def all_classes(request):
    """View to show all fitness classes, with filtering by category"""
    classes = FitnessClass.objects.all()
    categories = ClassCategory.objects.all()
    current_category = None
    search_query = None
    sort = None
    direction = None
    
    if request.GET:
        if 'category' in request.GET:
            category_name = request.GET['category']
            classes = classes.filter(category__name=category_name)
            current_category = ClassCategory.objects.get(name=category_name)
        
        if 'q' in request.GET:
            search_query = request.GET['q']
            if search_query:
                queries = Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(instructor__icontains=search_query)
                classes = classes.filter(queries)
        
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortkey = sort
            
            if sortkey == 'name':
                sortkey = 'name'
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            classes = classes.order_by(sortkey)
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'classes': classes,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'classes/all_classes.html', context)


def class_detail(request, class_id):
    """View to show individual class details"""
    fitness_class = get_object_or_404(FitnessClass, pk=class_id)
    
    context = {
        'fitness_class': fitness_class,
    }
    
    return render(request, 'classes/class_detail.html', context)
