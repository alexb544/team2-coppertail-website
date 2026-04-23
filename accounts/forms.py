from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory
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
        fields = ["avatar","phone_number", "address"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}), 
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "breed", "age", "image", "size", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}), 
            "breed": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}), 
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "size": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }


DogFormSet = inlineformset_factory(Profile, Dog, form=DogForm, extra=0, can_delete=True)

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs={
            'placeholder': 'Username', # Your Placeholder
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Password', # Your Placeholder
            'class': 'form-control',
            'id': 'password',
        })
    )
    
    remember_me = forms.BooleanField(required=False)

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your dog...',
            'class': 'form-control',
            'rows': 4
        })
    )
