from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""

    def test_profile_created_on_user_creation(self):
        """Test profile is automatically created when user is created"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@test.com'
        )
        # Trigger the signal or create manually if needed
        UserProfile.objects.get_or_create(user=user)
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), f"{user.username}'s profile")

    def test_profile_fields(self):
        """Test profile fields can be updated"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = '1234567890'
        profile.fitness_goals = 'Lose weight'
        profile.save()
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.fitness_goals, 'Lose weight')


class UserProfileFormTest(TestCase):
    """Test UserProfile form"""

    def test_form_valid_data(self):
        """Test form is valid with correct data"""
        form_data = {
            'phone_number': '1234567890',
            'fitness_goals': 'Build muscle',
            'emergency_contact_name': 'John Doe',
            'emergency_contact_phone': '0987654321'
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_fields(self):
        """Test form has correct fields"""
        form = UserProfileForm()
        expected_fields = [
            'phone_number',
            'date_of_birth',
            'fitness_goals',
            'emergency_contact_name',
            'emergency_contact_phone'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)


class ProfileViewTest(TestCase):
    """Test profile views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )

    def test_profile_view_requires_login(self):
        """Test profile page requires authentication"""
        response = self.client.get(reverse('profiles:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_update(self):
        """Test user can update their profile"""
        self.client.login(username='testuser', password='testpass123')
        UserProfile.objects.get_or_create(user=self.user)
        self.client.post(
            reverse('profiles:profile'),
            {
                'phone_number': '1234567890',
                'fitness_goals': 'Get fit'
            }
        )
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '1234567890')
