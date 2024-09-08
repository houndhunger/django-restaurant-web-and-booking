from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    quiet = forms.BooleanField(required=False)
    outside = forms.BooleanField(required=False)
    bench_seating = forms.BooleanField(required=False)
    disabled_access = forms.BooleanField(required=False)

    class Meta:
        model = Reservation
        exclude = ['user']  # Exclude user from the form
        fields = ['reservation_date', 'guest_count', 'note']  # Add all necessary fields here 
        # No 'tables' yet
        widgets = {
            'reservation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
