from django import forms
from .models import Reservation
#from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm # switching to this allauth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    def save(self, request):
        # Save the parent form (allauth form)
        user = super(CustomSignupForm, self).save(request)

        # Add first and last name to user object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        return user


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

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, label='Name')
#     last_name = forms.CharField(max_length=30, required=True, label='Surname')
#     #email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


# class CustomUserCreationForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, required=True, label='Name')
#     last_name = forms.CharField(max_length=30, required=True, label='Surname')
#     email = forms.EmailField(required=False)
#     password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
#         labels = {
#             'first_name': 'Name',
#             'last_name': 'Surname',
#             'email': 'Email',
#         }
#         widgets = {
#             'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
#         }

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
