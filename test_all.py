"""
Comprehensive automated tests for FitForge
Tests cover: Models, Views, Forms, Business Logic, Authentication, CRUD, E-commerce
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, time, timedelta
from decimal import Decimal
# Import all models
from bookings.models import Booking
from classes.models import FitnessClass, ClassSchedule
from memberships.models import MembershipTier
from products.models import Product
from checkout.models import Order, OrderLineItem


class ModelTests(TestCase):
    """Test all models can be created and have correct relationships"""

    def test_fitness_class_model(self):
        """Test FitnessClass model"""
        fc = FitnessClass.objects.create(
            name='Yoga',
            description='Relaxing yoga',
            duration=60,
            difficulty='beginner',
            instructor='John Doe',
            max_capacity=15
        )
        self.assertEqual(str(fc), 'Yoga')
        self.assertEqual(fc.max_capacity, 15)

    def test_class_schedule_model(self):
        """Test ClassSchedule model"""
        fc = FitnessClass.objects.create(
            name='HIIT',
            description='High intensity',
            duration=45,
            difficulty='advanced',
            instructor='Jane Smith',
            max_capacity=20
        )
        schedule = ClassSchedule.objects.create(
            fitness_class=fc,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(10, 45)
        )
        self.assertEqual(schedule.available_spots, 20)  # Auto-set from max_capacity

    def test_membership_tier_model(self):
        """Test MembershipTier model"""
        tier = MembershipTier.objects.create(
            name='Basic',
            description='Basic membership',
            price=Decimal('50.00'),
            duration='monthly',
            classes_per_week=3
        )
        self.assertEqual(tier.name, 'Basic')
        self.assertEqual(tier.classes_per_week, 3)

    def test_product_model(self):
        """Test Product model (CRUD - Create)"""
        product = Product.objects.create(
            name='Protein Powder',
            description='High quality protein',
            price=Decimal('35.99')
        )
        self.assertEqual(product.name, 'Protein Powder')
        self.assertEqual(product.price, Decimal('35.99'))

    def test_order_model(self):
        """Test Order model for e-commerce"""
        order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            country='Test Country'
        )
        self.assertTrue(order.order_number)  # Auto-generated
        self.assertEqual(order.full_name, 'Test User')

    def test_booking_model(self):
        """Test Booking model"""
        user = User.objects.create_user(username='testuser', password='pass')
        fc = FitnessClass.objects.create(
            name='Yoga',
            description='Test',
            duration=60,
            instructor='Test',
            max_capacity=10
        )
        schedule = ClassSchedule.objects.create(
            fitness_class=fc,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(11, 0)
        )
        booking = Booking.objects.create(
            user=user,
            class_schedule=schedule,
            status='confirmed'
        )
        self.assertEqual(booking.status, 'confirmed')


class AuthenticationTests(TestCase):
    """Test user authentication and authorization"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )

    def test_login_required_for_bookings(self):
        """Test bookings page requires login"""
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_login_required_for_profile(self):
        """Test profile page requires login"""
        response = self.client.get(reverse('profiles:profile'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_access(self):
        """Test authenticated user can access protected pages"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 200)


class CRUDOperationsTests(TestCase):
    """Test Create, Read, Update, Delete operations"""

    def test_create_product(self):
        """Test creating a product (CREATE)"""
        Product.objects.create(
            name='Test Product',
            price=Decimal('25.00')
        )
        self.assertEqual(Product.objects.count(), 1)

    def test_read_product(self):
        """Test reading products (READ)"""
        Product.objects.create(name='Product 1', price=Decimal('10.00'), sku='SKU001')
        Product.objects.create(name='Product 2', price=Decimal('20.00'), sku='SKU002')
        products = Product.objects.all()
        self.assertEqual(products.count(), 2)

    def test_update_product(self):
        """Test updating a product (UPDATE)"""
        product = Product.objects.create(name='Old Name', price=Decimal('10.00'))
        product.name = 'New Name'
        product.save()
        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.name, 'New Name')

    def test_delete_product(self):
        """Test deleting a product (DELETE)"""
        product = Product.objects.create(name='To Delete', price=Decimal('10.00'))
        product_id = product.id
        product.delete()
        self.assertFalse(Product.objects.filter(id=product_id).exists())


class ECommerceTests(TestCase):
    """Test e-commerce functionality with Stripe"""

    def test_order_creation_with_products(self):
        """Test order with line items"""
        order = Order.objects.create(
            full_name='Customer',
            email='customer@test.com',
            phone_number='123456',
            street_address1='Address',
            town_or_city='City',
            country='Country'
        )
        product = Product.objects.create(name='Item', price=Decimal('50.00'))
        line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )
        self.assertEqual(line_item.lineitem_total, Decimal('100.00'))


class ViewTests(TestCase):
    """Test views render correctly"""

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_classes_page(self):
        """Test classes page loads"""
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
        """Test products page loads"""
        response = self.client.get(reverse('products:all_products'))
        self.assertEqual(response.status_code, 200)

    def test_membership_plans_page(self):
        """Test membership plans page loads"""
        response = self.client.get('/memberships/')
        self.assertEqual(response.status_code, 200)


class BusinessLogicTests(TestCase):
    """Test custom business logic"""

    def test_order_total_calculation(self):
        """Test order total is calculated correctly"""
        order = Order.objects.create(
            full_name='Test',
            email='test@test.com',
            phone_number='123',
            street_address1='123 St',
            town_or_city='City',
            country='Country'
        )
        product = Product.objects.create(name='Item', price=Decimal('25.00'))
        OrderLineItem.objects.create(order=order, product=product, quantity=2)
        order.update_total()
        self.assertEqual(order.order_total, Decimal('50.00'))

    def test_class_schedule_spots_auto_set(self):
        """Test available spots auto-set from class capacity"""
        fc = FitnessClass.objects.create(
            name='Test',
            description='Test',
            duration=60,
            instructor='Test',
            max_capacity=15
        )
        schedule = ClassSchedule.objects.create(
            fitness_class=fc,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0)
        )
        self.assertEqual(schedule.available_spots, 15)


print("✅ All tests defined successfully")
