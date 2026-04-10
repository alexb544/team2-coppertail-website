from django.test import TestCase
from accounts.views import CustomLoginView, register, accounts
from django.urls import reverse, resolve

class URLTest(TestCase):

    def test_register_url_resolves_to_register_view(self):
        """Test that the register URL resolves to the register view"""
        url = reverse("accounts:register")
        resolver = resolve(url)
        self.assertEqual(resolver.func, register)

    def test_accounts_url_resolves_to_accounts_view(self):
        """Test that the accounts URL resolves to the accounts view"""
        url = reverse("accounts:accounts")
        resolver = resolve(url)
        self.assertEqual(resolver.func, accounts)

    def test_login_url_resolves_to_custom_login_view(self):
        """Test that the login URL resolves to CustomLoginView"""
        url = reverse("accounts:login")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CustomLoginView)
