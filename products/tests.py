from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from decimal import Decimal


class ProductModelTest(TestCase):
    """Test Product model"""

    def test_product_creation(self):
        """Test product can be created"""
        product = Product.objects.create(
            sku='TEST123',
            name='Test Product',
            description='Test description',
            price=Decimal('29.99')
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.price, Decimal('29.99'))

    def test_product_without_category(self):
        """Test product can exist without category"""
        product = Product.objects.create(
            name='No Category Product',
            description='Test',
            price=Decimal('19.99')
        )
        self.assertIsNone(product.category)


class ProductViewTest(TestCase):
    """Test product views"""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('29.99')
        )

    def test_all_products_view(self):
        """Test all products page loads"""
        response = self.client.get(reverse('products:all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/all_products.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        """Test product detail page loads"""
        url = reverse('products:product_detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_add_product_requires_superuser(self):
        """Test adding product requires superuser"""
        User.objects.create_user(
            username='regular',
            password='testpass'
        )
        self.client.login(username='regular', password='testpass')
        response = self.client.get(reverse('products:add_product'))
        self.assertEqual(response.status_code, 302)

    def test_edit_product_requires_superuser(self):
        """Test editing product requires superuser"""
        User.objects.create_user(
            username='regular',
            password='testpass'
        )
        self.client.login(username='regular', password='testpass')
        url = reverse('products:edit_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
