from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Dog


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}), 
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "breed", "age", "size", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}), 
            "breed": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}), 
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }