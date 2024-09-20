from django import forms
from .models import Reservation
#from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm # switching to this allauth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



"""
Signup Form
"""
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'id_email'}))

    def clean_email(self):
        # Validate that the email address is unique.
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def save(self, request):
        # Save the parent form (allauth form)
        user = super(CustomSignupForm, self).save(request)

        # Add first and last name to user object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        return user


"""
Reservation Form
"""
class ReservationForm(forms.ModelForm):
    reservation_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y/%m/%d %H:%M']
    )

    PREFERENCE_CHOICES = [
        ('no_preference', 'No Preference'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    is_quiet = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial='no_preference')
    us_outside = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial='no_preference')
    has_bench_seating = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial='no_preference')
    has_disabled_access = forms.ChoiceField(choices=PREFERENCE_CHOICES, required=False, initial='no_preference')

    class Meta:
        model = Reservation
        exclude = ['user']  # Exclude user from the form
        fields = ['reservation_date', 'guest_count', 'note', 'is_quiet', 'is_outside', 'has_bench_seating', 'has_disabled_access']
        # No 'tables' yet
        widgets = {
            'reservation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get('reservation_date')
        # Check if the minutes are a multiple of 5
        if reservation_date.minute % 5 != 0:
            raise ValidationError('Reservation time must be in 5-minute increments.')
        return reservation_date

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get('reservation_date')
        if reservation_date:
            # Set bounds for reservation time
            if reservation_date < timezone.now().replace(hour=9, minute=0) or reservation_date > timezone.now().replace(hour=22, minute=0):
                raise ValidationError("Reservations can only be made between 09:00 and 22:00.")
        return reservation_date

    def clean_guest_count(self):
        guest_count = self.cleaned_data.get('guest_count')
        max_guests = 12
        if guest_count > max_guests:
            raise forms.ValidationError(
                f"For reservations of more than {max_guests} guests, please contact the restaurant directly."
            )
        return guest_count
    
    def form_invalid(self, form):
        return self.render_to_response({'form': form})

