from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import Profile
from accounts.forms import UserRegisterForm
from django.urls import reverse

User = get_user_model()

class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:register")

    def test_register_get(self):
        """Test that GET returns 200 and renders the registration form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context["form"], UserRegisterForm)

    def test_register_post_valid(self):
        """Test that valid POST creates a user and redirects to login"""
        response = self.client.post(self.url, {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_post_valid_creates_profile(self):
        """Test that valid registration also auto-creates a Profile via signal"""
        self.client.post(self.url, {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        user = User.objects.get(username="newuser")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_post_invalid(self):
        """Test that invalid POST re-renders the form without creating a user"""
        response = self.client.post(self.url, {
            "username": "",
            "email": "bad-email",
            "password1": "pass",
            "password2": "different",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(User.objects.filter(email="bad-email").exists())

    def test_register_post_shows_success_message(self):
        """Test that successful registration flashes a success message"""
        response = self.client.post(self.url, {
            "username": "newuser",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }, follow=True)
        messages = list(response.context["messages"])
        self.assertTrue(any("newuser" in str(m) for m in messages))


class AccountsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:accounts")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_accounts_get_returns_200(self):
        """Test that GET returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_accounts_uses_correct_template(self):
        """Test that the view renders accounts/home.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "accounts/home.html")

    def test_accounts_context_contains_userinfo(self):
        """Test that context contains userinfo"""
        response = self.client.get(self.url)
        self.assertIn("userinfo", response.context)

    def test_accounts_context_contains_dogs(self):
        """Test that context contains dogs"""
        response = self.client.get(self.url)
        self.assertIn("dogs", response.context)

    def test_accounts_context_page_title(self):
        """Test that context contains the correct page_title"""
        response = self.client.get(self.url)
        self.assertEqual(response.context["page_title"], "Coppertail Grooming")


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("accounts:login")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_login_get(self):
        """Test that GET returns 200 and renders the login template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_post_valid(self):
        """Test that valid credentials log in and redirect to accounts page"""
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("accounts:accounts"))

    def test_login_post_invalid(self):
        """Test that invalid credentials re-render the login page"""
        response = self.client.post(self.url, {
            "username": "testuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
