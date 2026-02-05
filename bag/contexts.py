from decimal import Decimal
from django.conf import settings
from products.models import Product


def bag_contents(request):
    """
    Context processor to make bag contents available across all templates
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = Product.objects.get(pk=item_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    # Delivery calculation
    delivery_threshold = Decimal(settings.FREE_DELIVERY_THRESHOLD)
    delivery_cost = Decimal(settings.STANDARD_DELIVERY_COST)
    
    if total < delivery_threshold:
        delivery = delivery_cost
        free_delivery_delta = delivery_threshold - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': delivery_threshold,
        'grand_total': grand_total,
    }

    return context
