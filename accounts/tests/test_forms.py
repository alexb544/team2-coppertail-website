from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, DogForm

User = get_user_model()

class UserRegisterFormTest(TestCase):

    def get_valid_data(self):
        return {
                "username": "newuser",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!"
        }

    def test_valid_form(self):
        """Test that form is valid with all correct fields"""
        form = UserRegisterForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        """Test that form is invalid without a username"""
        data = self.get_valid_data()
        data["username"] = ""
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_missing_email(self):
        """Test that form is invalid without an email"""
        data = self.get_valid_data()
        data["email"] = ""
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_email(self):
        """Test that form is invalid with a malformed email"""
        data = self.get_valid_data()
        data["email"] = "not-an-email"
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_mismatch(self):
        """Test that form is invalid when passwords don't match"""
        data  = self.get_valid_data()
        data["password2"] = "DifferentPass!"
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        """Test that form is invalid if username already exists"""
        User.objects.create_user(username="newuser", password="testpass123")
        form = UserRegisterForm(data=self.get_valid_data())
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_saves_user(self):
        """Test that a valid form creates a User in the database"""
        form = UserRegisterForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid)
        user = form.save()
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, "newuser")

class ProfileUpdateFormTest(TestCase):

    def test_valid_form(self):
        """Test that form is valid with a phone number and address"""
        form = ProfileUpdateForm(data={
            "phone_number": "1234567890",
            "address": "123 Main St"
        })
        self.assertTrue(form.is_valid())

    def test_blank_field_allowed(self):
        """Test that both fields are optional"""
        form = ProfileUpdateForm(data={
            "phone_number": "",
            "address": ""
            })

    def test_phone_number_too_long(self):
        """Test that phone number exceeding 20 chars is invalid"""
        form = ProfileUpdateForm(data={
            "phone_number": "1" * 21,
            "address": ""
            })
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_address_too_long(self):
        """Test that address exceeding 80 chars is invalid"""
        form = ProfileUpdateForm(data={
            "phone_number": "",
            "address": "a" * 81
            })
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)

class UserUpdateFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="existinguser",
            password="testpass123",
            email="old@example.com"
        )

    def test_valid_form(self):
        """Test that form is valid with a username and email"""
        form = UserUpdateForm(
            data={
                "username": "updateduser",
                "email": "new@example.com"
            },
            instance=self.user
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Test that form is invalid with a malformed email"""
        form = UserUpdateForm(
            data={
                "username": "updateduser",
                "email": "not-an-email"},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_username(self):
        """Test that form is invalid without a username"""
        form = UserUpdateForm(
            data={
                "username": "",
                "email": "new@example.com"
                },
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class DogFormTest(TestCase):

    def test_valid_form(self):
        """Test that form is valid with just a name"""
        form = DogForm(data={
            "name": "Buddy",
            "breed": "",
            "age": "",
            "size": "MEDIUM",
            "notes": ""
            })
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Test that form is invalid without a name"""
        form = DogForm(data={
            "name": "",
            "breed": "Poodle",
            "age": 2,
            "size": "MEDIUM",
            "notes": ""
            })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_negative_age_invalid(self):
        """Test that a negative age fails form validation"""
        form = DogForm(data={
            "name": "Rex",
            "breed": "",
            "age": -1,
            "size": "MEDIUM",
            "notes": ""
            })
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_optional_fields_can_be_blank(self):
        """Test that breed, age, and notes are all optional"""
        form = DogForm(data={
            "name": "Max",
            "breed": "",
            "age": "",
            "size": "MEDIUM",
            "notes": ""})
        self.assertTrue(form.is_valid())
