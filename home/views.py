from django.shortcuts import render


def index(request):
    """View to return the home page"""
    return render(request, 'home/index.html')


def faq(request):
    """View for FAQ page"""
    return render(request, 'faq.html')


def terms(request):
    """View for Terms & Conditions page"""
    return render(request, 'terms.html')


def privacy(request):
    """View for Privacy Policy page"""
    return render(request, 'privacy.html')


def contact(request):
    """View for Contact Us page"""
    return render(request, 'contact.html')
