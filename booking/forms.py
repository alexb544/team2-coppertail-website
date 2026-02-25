from django import forms
from .models import Booking, TimeSlot
from accounts.models import Dog
#from services.models import Service # TODO: UNCOMMENT ONCE SERVICES MODEL IS DONE

class BookingCreateForm(forms.Form):
    slot = forms.ModelChoiceField(queryset=TimeSlot.objects.none())
    dog = forms.ModelChoiceField(queryset=Dog.objects.none())
    # TODO: UNCOMMENT ONCE SERVICES MODEL IS DONE
    # services = forms.ModelMultipleChoiceField(
    #     queryset=Service.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = TimeSlot.objects.filter(is_open=True)
        self.fields["dog"].queryset = Dog.objects.filter(user=user).order_by("name")