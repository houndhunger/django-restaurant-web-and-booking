from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    PREFERENCE_CHOICES = [
        (0, 'No Preference'),
        (1, 'Yes'),
        (2, 'No'),
    ]
    
    quiet = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial=0)
    outside = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial=0)
    bench_seating = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial=0)
    disabled_access = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial=0)

    class Meta:
        model = Reservation
        exclude = ['user']  # Exclude user from the form
        fields = ['reservation_date', 'guest_count', 'note']  # Add all necessary fields here 
        # No 'tables' yet
        widgets = {
            'reservation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
