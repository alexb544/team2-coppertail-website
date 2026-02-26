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
        self.fields["slot"].queryset = TimeSlot.objects.filter(is_open=True).order_by("start_time")
        self.fields["dog"].queryset = Dog.objects.filter(owner__user=user).order_by("name")
        self.fields["slot"].label_from_instance = self._slot_label

    @staticmethod
    def _slot_label(slot):
        start = slot.start_time.strftime("%A, %B %d, %Y at %I:%M %p")
        end = slot.end_time.strftime("%I:%M %p")
        return f"{start} to {end}"
