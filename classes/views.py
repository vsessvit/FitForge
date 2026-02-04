from django.shortcuts import render, get_object_or_404
from .models import FitnessClass, ClassCategory


def all_classes(request):
    """View to show all fitness classes, with filtering by category"""
    classes = FitnessClass.objects.all()
    categories = ClassCategory.objects.all()
    current_category = None
    
    if request.GET:
        if 'category' in request.GET:
            category_name = request.GET['category']
            classes = classes.filter(category__name=category_name)
            current_category = ClassCategory.objects.get(name=category_name)
    
    context = {
        'classes': classes,
        'categories': categories,
        'current_category': current_category,
    }
    
    return render(request, 'classes/all_classes.html', context)


def class_detail(request, class_id):
    """View to show individual class details"""
    fitness_class = get_object_or_404(FitnessClass, pk=class_id)
    
    context = {
        'fitness_class': fitness_class,
    }
    
    return render(request, 'classes/class_detail.html', context)
