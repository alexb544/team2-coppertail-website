#Imports
from django import forms
# import for registration logic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        # This tells Django which fields to actually put in the database
        fields = ['username', 'first_name', 'last_name', 'email']

#Form class for updating user information
class UserUpdateForm(forms.ModelForm):
    #Handles how the form connects to the user model
    class Meta:
        #Alerts that the User model is being updated
        model = User
        #Specifies what User fields are editable
        fields = ['username','first_name', 'last_name', 'email']

#Form class for updating profile information
class ProfileUpdateForm(forms.ModelForm):
    #Handles how the form connects to the profile model
    class Meta:
        #Alerts that the Profile model is being updated
        model = Profile
        #Specifies what Profile fields are editable
        fields = ['phone', 'profile_picture', 'dog_name', 'dog_breed', 'dog_age']
