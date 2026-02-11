from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from memberships.models import Membership
import uuid


class Order(models.Model):
    """Model for customer orders"""
    order_number = models.CharField(
        max_length=32, null=False, editable=False, unique=True
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=40, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """Individual line item in an order"""
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    membership = models.ForeignKey(
        Membership, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.IntegerField(null=False, blank=False, default=1)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def __str__(self):
        if self.product:
            return f'SKU {self.product.sku} on order {self.order.order_number}'
        else:
            return f'{self.membership.name} on order {self.order.order_number}'
