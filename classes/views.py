from django.shortcuts import render
from .models import FitnessClass


def all_classes(request):
    """View to show all fitness classes"""
    classes = FitnessClass.objects.all()
    
    context = {
        'classes': classes,
    }
    
    return render(request, 'classes/all_classes.html', context)
