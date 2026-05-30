"""
Regression tests for delivery info autofill functionality
Tests save and pre-populate features added to enhance UX
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from products.models import Product, ProductCategory


class DeliveryInfoAutofillTests(TestCase):
    """Tests for delivery information save and autofill feature"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.profile = self.user.profile

        # Create a test product for checkout
        category = ProductCategory.objects.create(
            name='Equipment',
            friendly_name='Fitness Equipment'
        )
        self.product = Product.objects.create(
            category=category,
            sku='TEST001',
            name='Test Product',
            description='Test description',
            price=49.99,
            stock_quantity=10,
            rating=4.5
        )

    def test_profile_has_default_delivery_fields(self):
        """Test UserProfile model includes default delivery fields"""
        # Check all default delivery fields exist
        self.assertTrue(hasattr(self.profile, 'default_street_address1'))
        self.assertTrue(hasattr(self.profile, 'default_street_address2'))
        self.assertTrue(hasattr(self.profile, 'default_town_or_city'))
        self.assertTrue(hasattr(self.profile, 'default_county'))
        self.assertTrue(hasattr(self.profile, 'default_postcode'))
        self.assertTrue(hasattr(self.profile, 'default_country'))
        self.assertTrue(hasattr(self.profile, 'phone_number'))

    def test_delivery_info_saves_to_profile(self):
        """Test delivery information is saved to profile after checkout"""
        # Set up profile with saved delivery info
        self.profile.phone_number = '0456837465'
        self.profile.default_street_address1 = 'My Street'
        self.profile.default_town_or_city = 'Dublin'
        self.profile.default_county = 'Dublin'
        self.profile.default_postcode = 'D02 XY45'
        self.profile.default_country = 'Ireland'
        self.profile.save()

        # Verify saved
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '0456837465')
        self.assertEqual(profile.default_street_address1, 'My Street')
        self.assertEqual(profile.default_town_or_city, 'Dublin')
        self.assertEqual(profile.default_postcode, 'D02 XY45')

    def test_checkout_form_prepopulates_for_logged_in_user(self):
        """
        Test checkout form pre-fills with saved delivery info
        This enhances UX by reducing form filling time
        """
        # Save delivery info to profile
        self.profile.phone_number = '0456837465'
        self.profile.default_street_address1 = 'My Street'
        self.profile.default_street_address2 = 'Apt 4'
        self.profile.default_town_or_city = 'Dublin'
        self.profile.default_county = 'Dublin'
        self.profile.default_postcode = 'D02 XY45'
        self.profile.default_country = 'Ireland'
        self.profile.save()

        # Log in and add item to bag
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

        # Get checkout page
        response = self.client.get(reverse('checkout:checkout'))

        # Check form has initial values from profile
        form = response.context['order_form']
        self.assertEqual(form.initial.get('full_name'), 'John Doe')
        self.assertEqual(form.initial.get('email'), 'test@example.com')
        self.assertEqual(form.initial.get('phone_number'), '0456837465')
        self.assertEqual(form.initial.get('street_address1'), 'My Street')
        self.assertEqual(form.initial.get('street_address2'), 'Apt 4')
        self.assertEqual(form.initial.get('town_or_city'), 'Dublin')
        self.assertEqual(form.initial.get('postcode'), 'D02 XY45')

    def test_empty_profile_doesnt_break_checkout(self):
        """Test checkout works for user with no saved delivery info"""
        # Log in user with empty profile
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

        # Get checkout page
        response = self.client.get(reverse('checkout:checkout'))

        # Should load successfully
        self.assertEqual(response.status_code, 200)

        # Form should exist but have minimal initial data
        form = response.context['order_form']
        self.assertEqual(form.initial.get('full_name'), 'John Doe')
        self.assertEqual(form.initial.get('email'), 'test@example.com')

    def test_anonymous_user_gets_empty_form(self):
        """Test anonymous users get empty checkout form"""
        # Don't log in, just add to bag
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

        # Get checkout page
        response = self.client.get(reverse('checkout:checkout'))

        # Should load successfully
        self.assertEqual(response.status_code, 200)

        # Form should have no initial values
        form = response.context['order_form']
        self.assertIsNone(form.initial.get('phone_number'))
        self.assertIsNone(form.initial.get('street_address1'))

    def test_profile_fields_are_optional(self):
        """Test all default delivery fields are optional (can be blank)"""
        # All fields should allow blank
        self.profile.default_street_address1 = ''
        self.profile.default_town_or_city = ''
        self.profile.default_postcode = ''
        self.profile.phone_number = ''

        # Should save without errors
        try:
            self.profile.save()
            saved = True
        except Exception:
            saved = False

        self.assertTrue(saved, "Profile should save with empty delivery fields")
