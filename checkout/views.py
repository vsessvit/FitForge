from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm


def checkout(request):
    """Handle checkout process"""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    
    bag = request.session.get('bag', {})
    
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect('products:product_list')
    
    order_form = OrderForm()
    
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
    }
    
    return render(request, 'checkout/checkout.html', context)
