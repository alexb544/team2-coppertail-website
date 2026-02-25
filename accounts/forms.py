#Imports
from django import forms
from django.contrib.auth.models import User
from .models import Profile

#Form class for updating user information
class UserUpdateForm(forms.ModelForm):
    #Handles how the form connects to the user model
    class Meta:
        #Alerts that the User model is being updated
        model = User
        #Specifies what User fields are editable
        fields = ['username', 'email']

#Form class for updating profile information
class ProfileUpdateForm(forms.modelForm):
    #Handles how the form connects to the profile model
    class Meta:
        #Alerts that the Profile model is being updated
        model = Profile
        #Specifies what Profile fields are editable
        fields = ['phone', 'profile_picture', 'dog_name', 'dog_breed', 'dog_age']
