#Importing needed classes
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile, Dog

#Assigns the User model to a variable for easy reuse
User = get_user_model()

#A test case class for testing the Profile model, it inherits from TestCase
class ProfileModelTest(TestCase):
    #A method that sets up inital data needed for all tests
    def setUp(self):
        #Create a user for testing and assigns it to self.user so it can be used for all test methods
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        #Create a profile for testing that is linked to the user we just created, it is assigned to self.profile so it can be used for all test methods
        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="123-456-7890",
            address="123 Main St"
        )

    def test_profile_creation(self):
        """Test that a profile is created successfully"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, "555-1234")
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
        profile = Profile.objects.create(user=user_no_name)
        self.assertEqual(str(profile), "noname")

    def test_profile_blank_fields(self):
        """Test that phone_number and address can be blank"""
        profile = Profile.objects.create(user=self.user)
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


class DogModelTest(TestCase):
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create_user(
            username="dogowner",
            password="testpass123"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            phone_number="555-5678"
        )
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
            name="Notey",
            notes=long_notes
        )
        self.assertEqual(dog.notes, long_notes)


class ProfileDogIntegrationTest(TestCase):
    """Test the relationship between Profile and Dog models"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username="owner1", password="pass")
        self.user2 = User.objects.create_user(username="owner2", password="pass")
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_different_owners_different_dogs(self):
        """Test that different profiles can have dogs with the same name"""
        dog1 = Dog.objects.create(owner=self.profile1, name="Buddy")
        dog2 = Dog.objects.create(owner=self.profile2, name="Buddy")
        
        self.assertNotEqual(dog1.id, dog2.id)
        self.assertEqual(str(dog1), "Buddy (owner1)")
        self.assertEqual(str(dog2), "Buddy (owner2)")

    def test_cascade_from_user_to_dogs(self):
        """Test complete cascade: User -> Profile -> Dogs"""
        Dog.objects.create(owner=self.profile1, name="Dog1")
        Dog.objects.create(owner=self.profile1, name="Dog2")
        
        # Verify dogs exist
        self.assertEqual(Dog.objects.filter(owner=self.profile1).count(), 2)
        
        # Delete the user
        self.user1.delete()
        
        # Verify profile and dogs are also deleted
        self.assertEqual(Profile.objects.filter(user=self.user1).count(), 0)
        self.assertEqual(Dog.objects.filter(owner=self.profile1).count(), 0)

