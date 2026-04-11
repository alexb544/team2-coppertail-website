from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class SignalTest(TestCase):

    def test_profile_auto_created_user_creation(self):
        """Test that creating a User automatically creates a linked Profile"""
        user = User.objects.create_user(username="test", password="testpass123")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_not_duplicated_user_save(self):
        """Test that saving an existing User does not create a second Profile"""
        user = User.objects.create_user(username="test", password="testpass123")
        user.first_name = "Updated"
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
