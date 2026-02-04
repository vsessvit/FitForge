from django.shortcuts import render


def index(request):
    """View to return the home page"""
    return render(request, 'home/index.html')
