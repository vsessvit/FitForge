from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from bag.contexts import bag_contents
from products.models import Product
from memberships.models import MembershipTier
from .forms import OrderForm
from .models import Order, OrderLineItem
import stripe
import logging

logger = logging.getLogger(__name__)


def checkout(request):
    """Handle checkout process"""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    
    if request.method == 'POST':
        bag = request.session.get('bag', {})
        membership_id = request.session.get('membership_in_bag', None)
        
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            # Create order line items for products
            for item_id, quantity in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('bag:view_bag'))
                except Exception as e:
                    logger.error(f"Error creating order line item for product {item_id}: {str(e)}")
                    messages.error(request, "There was an error processing your order. Please try again.")
                    order.delete()
                    return redirect(reverse('bag:view_bag'))
            
            # Create order line item for membership if present
            if membership_id:
                try:
                    membership = MembershipTier.objects.get(id=membership_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        membership=membership,
                        quantity=1,
                    )
                    order_line_item.save()
                except MembershipTier.DoesNotExist:
                    messages.error(request, (
                        "The membership in your bag wasn't found. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('bag:view_bag'))
                except Exception as e:
                    logger.error(f"Error creating order line item for membership {membership_id}: {str(e)}")
                    messages.error(request, "There was an error processing your order. Please try again.")
                    order.delete()
                    return redirect(reverse('bag:view_bag'))
            
            return redirect(reverse('checkout:checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            logger.warning(f"Invalid checkout form: {order_form.errors}")
    else:
        bag = request.session.get('bag', {})
        
        if not bag and not request.session.get('membership_in_bag'):
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect('products:product_list')
        
        order_form = OrderForm()
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    
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
        logger.error(f"Error creating payment intent: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


def checkout_success(request, order_number):
    """Handle successful checkouts"""
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    # Clear the bag from session
    if 'bag' in request.session:
        del request.session['bag']
    if 'membership_in_bag' in request.session:
        del request.session['membership_in_bag']
    
    context = {
        'order': order,
    }
    
    return render(request, 'checkout/checkout_success.html', context)
