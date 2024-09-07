from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['user']  # Exclude user from the form
        fields = ['reservation_date', 'guest_count', 'note']  # Add all necessary fields here 
        # No 'tables' yet
        widgets = {
            'reservation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
