from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, Mock
from decimal import Decimal
from checkout.models import Order, OrderLineItem
from products.models import Product


class OrderModelTest(TestCase):
    """Test Order model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_order_creation(self):
        """Test order can be created"""
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country',
            order_total=Decimal('50.00'),
            grand_total=Decimal('50.00')
        )
        self.assertTrue(order.order_number)
        self.assertEqual(order.full_name, 'Test User')

    def test_order_number_generation(self):
        """Test order number is automatically generated"""
        order1 = Order.objects.create(
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country'
        )
        order2 = Order.objects.create(
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country'
        )
        self.assertNotEqual(order1.order_number, order2.order_number)

    def test_order_total_calculation(self):
        """Test order total is calculated correctly"""
        order = Order.objects.create(
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country'
        )
        product = Product.objects.create(
            name='Test Product',
            price=Decimal('25.00')
        )
        OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )
        order.update_total()
        self.assertEqual(order.order_total, Decimal('50.00'))


class CheckoutViewTest(TestCase):
    """Test checkout views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('25.00')
        )

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view_with_items(self, mock_stripe):
        """Test checkout page loads with items in bag"""
        mock_stripe.return_value = Mock(
            client_secret='test_secret',
            id='test_pi_id'
        )
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse('checkout:checkout'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_success_view(self):
        """Test checkout success page"""
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country'
        )
        url = reverse('checkout:checkout_success', args=[order.order_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
