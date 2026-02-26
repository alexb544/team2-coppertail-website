from django import forms
from .models import TimeSlot
from accounts.models import Dog
from services.models import Service

class BookingCreateForm(forms.Form):
    slot = forms.ModelChoiceField(queryset=TimeSlot.objects.none())
    dog = forms.ModelChoiceField(queryset=Dog.objects.none())
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = TimeSlot.objects.filter(is_open=True).order_by("start") # type: ignore
        self.fields["dog"].queryset = Dog.objects.filter(owner__user=user).order_by("name") # type: ignore