from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Dog
from django.forms import inlineformset_factory


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


#Form class for updating profile information
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}), 
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}), 
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class DogUpdateForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "breed", "age", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}), 
            "breed": forms.TextInput(attrs={"class": "form-control"}), 
            "age": forms.NumberInput(attrs={"class": "form-control"}), 
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }
        #DogFormSet = inlineformset_factory(Profile, Dog, form=DogUpdateForm, extra=0, can_delete=True)
            # ^^ was causing an error — don't know if needed or not
