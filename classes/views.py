from django.shortcuts import render
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
