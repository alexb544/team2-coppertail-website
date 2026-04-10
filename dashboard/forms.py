from django import forms
from services.models import Service
from booking.models import TimeSlot

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'base_price', 'description']
        widgets = {
            'service_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Full Groom'
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Describe the service...'
            }),
        }

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time', 'is_open']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
            'is_open': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
