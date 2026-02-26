#Imports
from django import forms
from .models import Profile, Dog

#Form class for updating profile information
class ProfileUpdateForm(forms.ModelForm):
    #Handles how the form connects to the Profile model
    class Meta:
        #Alerts that the Profile model is being updated
        model = Profile
        #Specifies what Profile fields are editable
        fields = ["phone_number", "address"]

        widgets = {"phone_number": forms.TextInput(ttrs={"class": "form-control"}), "address": forms.TextInput(attrs={"class": "form-control"},)}

#Form class for updating dog information
class DogUpdateForm(forms.modelForm):
    #Handles how the form connects to the Dog model
    class Meta:
        #Alerts that the Dog model is being updated
        model = Profile
        #Specifies what Dog fields are editable
        fields = ["name", "breed", "age", "notes"]

        widgets = {"name": forms.TextInput(attr={"class": "form-control"}), "breed": forms.TextInput(attrs={"class": "form-control"}), "age": forms.NumberInput(attrs={"class": "form-control"}), "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),}

        DogFormSet = inlineformset_factory(Profile, Dog, form=DogUpdateForm, extra=0, can_delete=True)
