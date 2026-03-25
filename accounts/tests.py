from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import Profile, Dog
from accounts.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, DogUpdateForm
from accounts.views import CustomLoginView, register, accounts
from django.urls import reverse, resolve

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        self.profile = self.user.profile
        self.profile.phone_number = "123-456-7890"
        self.profile.address = "123 Main St"
        self.profile.save()

    def test_profile_creation(self):
        """Test that a profile is created successfully"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, "123-456-7890")
        self.assertEqual(self.profile.address, "123 Main St")

    def test_profile_str_with_full_name(self):
        """Test __str__ returns full name when available"""
        expected = "John Doe"
        self.assertEqual(str(self.profile), expected)

    def test_profile_str_with_username_only(self):
        """Test __str__ returns username when full name is empty"""
        user_no_name = User.objects.create_user(
            username="noname",
            password="testpass123"
        )
        profile = user_no_name.profile
        self.assertEqual(str(profile), "noname")

    def test_profile_blank_fields(self):
        """Test that phone_number and address can be blank"""
        user2 = User.objects.create_user(username="blankuser", password="testpass123")
        profile = user2.profile
        self.assertEqual(profile.phone_number, "")
        self.assertEqual(profile.address, "")

    def test_profile_cascade_delete(self):
        """Test that profile is deleted when user is deleted"""
        profile_id = self.profile.id
        self.user.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=profile_id)

    def test_one_to_one_relationship(self):
        """Test that one user can only have one profile"""
        with self.assertRaises(Exception):
            # Attempting to create another profile for the same user should fail
            Profile.objects.create(user=self.user)

    def test_phone_number_max_length(self):
        """Test that phone number accepts up to 20 characters"""
        self.profile.phone_number = "1" * 20
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, "1" * 20)

    def test_address_max_length(self):
        """Test that address accepts up to 80 characters"""
        self.profile.address = "a" * 80
        self.profile.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.address, "a" * 80)

class DogModelTest(TestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create_user(
            username="dogowner",
            password="testpass123"
        )
        self.profile = self.user.profile
        self.profile.phone_number = "123-456-7890"
        self.profile.save()
        # Create a dog
        self.dog = Dog.objects.create(
            owner=self.profile,
            name="Buddy",
            breed="Golden Retriever",
            age=3,
            notes="Very friendly dog"
        )

    def test_dog_creation(self):
        """Test that a dog is created successfully"""
        self.assertEqual(self.dog.owner, self.profile)
        self.assertEqual(self.dog.name, "Buddy")
        self.assertEqual(self.dog.breed, "Golden Retriever")
        self.assertEqual(self.dog.age, 3)
        self.assertEqual(self.dog.notes, "Very friendly dog")

    def test_dog_str(self):
        """Test __str__ returns name and owner username"""
        expected = "Buddy (dogowner)"
        self.assertEqual(str(self.dog), expected)

    def test_dog_blank_optional_fields(self):
        """Test that breed, age, and notes can be blank/null"""
        dog = Dog.objects.create(
            owner=self.profile,
            name="Rex"
        )
        self.assertEqual(dog.breed, "")
        self.assertIsNone(dog.age)
        self.assertEqual(dog.notes, "")

    def test_dog_cascade_delete(self):
        """Test that dogs are deleted when profile is deleted"""
        dog_id = self.dog.id
        self.profile.delete()
        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(id=dog_id)

    def test_multiple_dogs_per_owner(self):
        """Test that one profile can have multiple dogs"""
        dog2 = Dog.objects.create(
            owner=self.profile,
            name="Max",
            breed="Beagle"
        )
        self.assertEqual(self.profile.dogs.count(), 2)
        self.assertIn(self.dog, self.profile.dogs.all())
        self.assertIn(dog2, self.profile.dogs.all())

    def test_related_name_dogs(self):
        """Test the related_name 'dogs' works correctly"""
        Dog.objects.create(owner=self.profile, name="Charlie")
        Dog.objects.create(owner=self.profile, name="Daisy")
        
        dogs = self.profile.dogs.all()
        self.assertEqual(dogs.count(), 3)  # Including Buddy from setUp
        dog_names = [dog.name for dog in dogs]
        self.assertIn("Buddy", dog_names)
        self.assertIn("Charlie", dog_names)
        self.assertIn("Daisy", dog_names)

    def test_dog_age_positive_integer(self):
        """Test that age accepts positive integers"""
        dog = Dog.objects.create(
            owner=self.profile,
            name="Puppy",
            age=1
        )
        self.assertEqual(dog.age, 1)

    def test_dog_with_long_notes(self):
        """Test that notes field accepts long text"""
        long_notes = "This is a very long note. " * 50
        dog = Dog.objects.create(
            owner=self.profile,
            name="Bella",
            notes=long_notes
        )
        self.assertEqual(dog.notes, long_notes)

    def test_dog_default_size(self):
        """Test that size defaults to MEDIUM"""
        size = Dog.Size.MEDIUM
        dog = Dog.objects.create(
                owner=self.profile,
                name="Regular"
        )
        self.assertEqual(dog.size, size)

    def test_dog_size_small(self):
        """Test that size can be set to SMALL"""
        size = Dog.Size.SMALL
        dog = Dog.objects.create(
                owner=self.profile,
                name="Smalls",
                size=Dog.Size.SMALL
        )
        self.assertEqual(dog.size, size)

    def test_dog_size_large(self):
        """Test that size can be set to LARGE"""
        size = Dog.Size.LARGE
        dog = Dog.objects.create(
                owner=self.profile,
                name="Big",
                size=Dog.Size.LARGE
        )
        self.assertEqual(dog.size, size)

    def test_dog_negative_age_fails_validation(self):
        """Test that negative age fails model validation"""
        dog = Dog(
                owner=self.profile,
                name="Falling",
                age=-1
                )
        with self.assertRaises(Exception):
            dog.full_clean()


class ProfileDogIntegrationTest(TestCase):
    """Test the relationship between Profile and Dog models"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username="owner1", password="pass")
        self.user2 = User.objects.create_user(username="owner2", password="pass")
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

    def test_different_owners_different_dogs(self):
        """Test that different profiles can have dogs with the same name"""
        dog1 = Dog.objects.create(owner=self.profile1, name="Buddy")
        dog2 = Dog.objects.create(owner=self.profile2, name="Charlie")
        
        self.assertNotEqual(dog1.id, dog2.id)
        self.assertEqual(str(dog1), "Buddy (owner1)")
        self.assertEqual(str(dog2), "Charlie (owner2)")

    def test_cascade_from_user_to_dogs(self):
        """Test complete cascade: User -> Profile -> Dogs"""
        Dog.objects.create(owner=self.profile1, name="Dog1")
        Dog.objects.create(owner=self.profile1, name="Dog2")
        
        # Verify dogs exist
        self.assertEqual(Dog.objects.filter(owner=self.profile1).count(), 2)

        #Save user and profile IDs
        user1_id = self.user1.id
        profile1_id = self.profile1.id
        
        # Delete the user
        self.user1.delete()
        
        # Verify profile and dogs are also deleted
        self.assertEqual(Profile.objects.filter(user_id=user1_id).count(), 0)
        self.assertEqual(Dog.objects.filter(owner_id=profile1_id).count(), 0)

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
 
 
class DogUpdateFormTest(TestCase):
 
    def test_valid_form(self):
        """Test that form is valid with just a name"""
        form = DogUpdateForm(data={
            "name": "Buddy", 
            "breed": "", 
            "age": "", 
            "notes": ""
            })
        self.assertTrue(form.is_valid())
 
    def test_missing_name(self):
        """Test that form is invalid without a name"""
        form = DogUpdateForm(data={
            "name": "", 
            "breed": "Poodle", 
            "age": 2, 
            "notes": ""
            })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
 
    def test_negative_age_invalid(self):
        """Test that a negative age fails form validation"""
        form = DogUpdateForm(data={
            "name": "Rex", 
            "breed": "", 
            "age": -1, 
            "notes": ""
            })
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)
 
    def test_optional_fields_can_be_blank(self):
        """Test that breed, age, and notes are all optional"""
        form = DogUpdateForm(data={
            "name": "Max", 
            "breed": "", 
            "age": "", 
            "notes": ""})
        self.assertTrue(form.is_valid())

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
