"""
Regression tests for stock validation fixes
Tests cumulative stock validation to prevent inventory bypass
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, ProductCategory


class StockValidationTests(TestCase):
    """Tests for cumulative stock validation bug fix"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = ProductCategory.objects.create(
            name='Equipment',
            friendly_name='Fitness Equipment'
        )
        self.product = Product.objects.create(
            category=self.category,
            sku='TEST001',
            name='Test Product',
            description='Test description',
            price=49.99,
            stock_quantity=10,  # Only 10 in stock
            rating=4.5
        )

    def test_add_within_stock_limit(self):
        """Test adding product within stock limit succeeds"""
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {
                'quantity': 5,
                'redirect_url': '/'
            }
        )
        self.assertEqual(response.status_code, 302)

        # Check item is in bag
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 5)

    def test_add_exceeding_stock_limit_single_action(self):
        """Test adding more than available stock in single action fails"""
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {
                'quantity': 15,  # More than 10 available
                'redirect_url': '/'
            },
            follow=True
        )

        # Should redirect with error
        self.assertEqual(response.status_code, 200)

        # Check error message appears
        messages = list(response.context['messages'])
        self.assertTrue(any('Only 10 available in stock' in str(m) for m in messages))

        # Bag should be empty
        bag = self.client.session.get('bag', {})
        self.assertNotIn(str(self.product.id), bag)

    def test_cumulative_stock_validation_prevents_bypass(self):
        """
        CRITICAL FIX: Test cumulative validation prevents stock bypass
        Previously users could add 5 items twice to bypass 10-item stock limit
        """
        # First add: 5 items
        self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {
                'quantity': 5,
                'redirect_url': '/'
            }
        )

        # Verify 5 items in bag
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 5)

        # Second add: Try to add 7 more (would exceed 10 stock)
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {
                'quantity': 7,
                'redirect_url': '/'
            },
            follow=True
        )

        # Should be rejected with error message
        messages = list(response.context['messages'])
        self.assertTrue(
            any('Cannot add 7 more' in str(m)
                and 'You have 5 in your bag' in str(m)
                and 'only 10 available in stock' in str(m)
                for m in messages),
            "Expected cumulative stock validation error message"
        )

        # Bag should still have only 5 items (not 12)
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 5)

    def test_adjust_bag_respects_stock_limit(self):
        """Test adjusting bag quantity also respects stock limits"""
        # Add 5 items first
        self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {
                'quantity': 5,
                'redirect_url': '/'
            }
        )

        # Try to adjust to 15 (exceeds stock)
        response = self.client.post(
            reverse('bag:adjust_bag', args=[self.product.id]),
            {
                'quantity': 15
            },
            follow=True
        )

        # Should show error
        messages = list(response.context['messages'])
        self.assertTrue(any('Cannot update' in str(m) and 'Only 10 available' in str(m) for m in messages))

        # Quantity should remain at 5
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 5)

    def test_add_up_to_exact_stock_limit(self):
        """Test can add items up to exact stock limit"""
        # Add 6 items
        self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {'quantity': 6, 'redirect_url': '/'}
        )

        # Add 4 more (total = 10, exactly at limit)
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {'quantity': 4, 'redirect_url': '/'}
        )

        # Should succeed
        self.assertEqual(response.status_code, 302)

        # Bag should have 10 items
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 10)

    def test_error_message_shows_current_bag_quantity(self):
        """Test error message includes helpful information about current bag state"""
        # Add 5 items first
        self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {'quantity': 5, 'redirect_url': '/'}
        )

        # Try to add 10 more (total would be 15, exceeds 10 stock)
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.product.id]),
            {'quantity': 10, 'redirect_url': '/'},
            follow=True
        )

        # Should get error message
        messages = list(response.context['messages'])
        self.assertTrue(len(messages) > 0, "Should have at least one message")

        # Check for error message (not success)
        has_error = any('Cannot add' in str(m) or 'only' in str(m).lower() for m in messages)
        self.assertTrue(has_error, f"Expected error message about stock, got: {[str(m) for m in messages]}")

        # Bag should still have only 5 items (not 15)
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 5)
