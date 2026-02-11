from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from bag.contexts import bag_contents
from .forms import OrderForm
import stripe


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


@require_POST
def create_payment_intent(request):
    """Create a Stripe payment intent"""
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Get bag contents and calculate total
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        
        # Stripe requires amount in cents
        stripe_total = round(total * 100)
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY if hasattr(settings, 'STRIPE_CURRENCY') else 'usd',
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
