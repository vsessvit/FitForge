from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product
from memberships.models import MembershipTier


def view_bag(request):
    """
    Display the shopping bag contents
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def add_membership_to_bag(request, membership_id):
    """
    Add a membership to the shopping bag (only one membership allowed)
    """
    membership = get_object_or_404(MembershipTier, pk=membership_id)
    redirect_url = request.POST.get('redirect_url', reverse('bag:view_bag'))
    
    # Store membership separately in session
    old_membership_id = request.session.get('membership_in_bag')
    if old_membership_id:
        try:
            old_membership = MembershipTier.objects.get(pk=old_membership_id)
            messages.info(request, f'Replaced {old_membership.name} with {membership.name}')
        except MembershipTier.DoesNotExist:
            pass
    else:
        messages.success(request, f'Added {membership.name} membership to your bag')
    
    request.session['membership_in_bag'] = str(membership_id)
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product in the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('bag:view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the specified product from the shopping bag
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return redirect(reverse('bag:view_bag'))
    
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect(reverse('bag:view_bag'))


def remove_membership_from_bag(request):
    """
    Remove the membership from the shopping bag
    """
    try:
        membership_id = request.session.get('membership_in_bag')
        if membership_id:
            membership = get_object_or_404(MembershipTier, pk=membership_id)
            del request.session['membership_in_bag']
            messages.success(request, f'Removed {membership.name} membership from your bag')
        
        return redirect(reverse('bag:view_bag'))
    
    except Exception as e:
        messages.error(request, f'Error removing membership: {e}')
        return redirect(reverse('bag:view_bag'))



