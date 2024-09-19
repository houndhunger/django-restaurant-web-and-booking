from django import forms
from .models import Reservation
#from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm # switching to this allauth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
