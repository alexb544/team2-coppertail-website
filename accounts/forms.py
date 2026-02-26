from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Dog
from django.forms import inlineformset_factory


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

#Form class for updating profile information
class ProfileUpdateForm(forms.ModelForm):
    #Handles how the form connects to the Profile model

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.modelForm):

    class Meta:
        model = Profile
        #Specifies what Profile fields are editable
        fields = ["phone_number", "address"]

        # FIXED: changed ttrs to attrs
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}), 
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }

#Form class for updating dog information
class DogUpdateForm(forms.ModelForm): # FIXED: capital M in ModelForm
    #Handles how the form connects to the Dog model
    class Meta:
        #Alerts that the Dog model is being updated
        model = Dog # FIXED: changed Profile to Dog
        #Specifies what Dog fields are editable
        fields = ["name", "breed", "age", "notes"]

        # FIXED: changed attr to attrs
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}), 
            "breed": forms.TextInput(attrs={"class": "form-control"}), 
            "age": forms.NumberInput(attrs={"class": "form-control"}), 
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

# DogFormSet logic
DogFormSet = inlineformset_factory(Profile, Dog, form=DogUpdateForm, extra=0, can_delete=True)

        fields = ['phone', 'profile_picture', 'dog_name', 'dog_breed', 'dog_age']

