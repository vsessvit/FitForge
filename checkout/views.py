from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """Handle checkout process"""
    bag = request.session.get('bag', {})
    
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect('products:product_list')
    
    order_form = OrderForm()
    
    context = {
        'order_form': order_form,
    }
    
    return render(request, 'checkout/checkout.html', context)
