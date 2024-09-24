from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import Reservation, OpeningTime
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from booking.models import ReservationTimeSpan
from datetime import datetime, timedelta, time
from .utils.reservation_utils import format_duration


class CustomSignupForm(SignupForm):
    """
    Custom Signup Form to add first and last name fields.
    """
    first_name = forms.CharField(
        max_length=30, label='First Name', required=True
    )
    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'id': 'id_email'})
    )

    def clean_email(self):
        """
        Validate that the email address is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "A user with this email address already exists."
            )
        return email

    def save(self, request):
        """
        Save the user and add first and last name to the user object.
        """
        user = super(CustomSignupForm, self).save(request)

        # Add first and last name to user object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user


class ReservationForm(forms.ModelForm):
    """
    Reservation Form to manage reservation details.
    """
    reservation_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'placeholder': 'YYYY/MM/DD HH:MM'}
        ),
        input_formats=['%Y/%m/%d %H:%M'],
        required=True
    )

    PREFERENCE_CHOICES = [
        ('no_preference', 'No specific preference'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    is_quiet = forms.ChoiceField(
        choices=PREFERENCE_CHOICES, required=False,
        initial='no_preference'
    )
    is_outside = forms.ChoiceField(
        choices=PREFERENCE_CHOICES, required=False,
        initial='no_preference'
    )
    has_bench_seating = forms.ChoiceField(
        choices=PREFERENCE_CHOICES, required=False,
        initial='no_preference'
    )
    has_disabled_access = forms.ChoiceField(
        choices=PREFERENCE_CHOICES, required=False,
        initial='no_preference'
    )

    guest_count = forms.IntegerField(required=True)

    class Meta:
        model = Reservation
        exclude = ['user']  # Exclude user from the form
        fields = [
            'reservation_date', 'guest_count', 'note', 'is_quiet',
            'is_outside', 'has_bench_seating', 'has_disabled_access'
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_guest_count(self):
        """
        Validate guest count to ensure it does not exceed the maximum limit.
        """
        guest_count = self.cleaned_data.get('guest_count')
        max_guests = 12
        if guest_count is None:
            raise forms.ValidationError("Guest count is required.")

        if guest_count > max_guests:
            raise forms.ValidationError(
                f"For reservations of more than {max_guests} guests, "
                "please contact the restaurant directly."
            )

        return guest_count

    def clean(self):
        """
        Validate reservation date to ensure it's not in the past
        and falls within allowed time range.
        """
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        guest_count = cleaned_data.get('guest_count')

        original_reservation = (
            self.instance if self.instance.pk else None
        )

        now = timezone.now()

        if not reservation_date:
            raise forms.ValidationError("Reservation date is required.")

        if reservation_date < now:
            raise forms.ValidationError(
                "Reservations cannot be made in the past."
            )

        # Validate if reservation fits within opening hours
        try:
            reservation_time_span = ReservationTimeSpan.objects.get(
                guest_count=guest_count
            )

            # Calculate reservation end time based on the time span
            reservation_end = reservation_date + reservation_time_span.duration
            cleaned_data['reservation_end_date'] = reservation_end
        except ReservationTimeSpan.DoesNotExist:
            raise forms.ValidationError(
                'Please contact the restaurant for large party sizes.'
            )
        
        # FORBID Find overlapping reservations considering a 2-hour overlap
        overlapping_reservations = Reservation.objects.filter(
            Q(reservation_date__lt=cleaned_data['reservation_end_date']) &
            Q(reservation_end_date__gt=reservation_date)
        ).exclude(pk=original_reservation.pk if original_reservation else None)

        if overlapping_reservations.exists():
            raise forms.ValidationError(
                'You already have an overlapping reservation for this time.'
            )

        # Get opening times for the reservation day
        reservation_day = reservation_date.strftime('%a').lower()
        opening_time = OpeningTime.objects.filter(
            day_of_week=reservation_day
        ).first()

        # If day entry for Opening times is missing
        if not opening_time or (
            opening_time.open_time == opening_time.close_time ==
            timezone.datetime.min.time()
        ):
            raise forms.ValidationError(
                'The restaurant is closed at the time of your reservation.'
            )

        # Logic for calculating reservation_fits_start and reservation_fits_end
        if opening_time.close_time >= time(4, 00):
            reservation_fits_start = (
                opening_time.open_time <= reservation_date.time() <=
                opening_time.close_time
            )
            reservation_fits_end = (
                reservation_date.time() <= reservation_end.time() <=
                opening_time.close_time
            )
        else:
            reservation_fits_start = (
                opening_time.open_time <= reservation_date.time() <=
                time(23, 59)
            )
            reservation_fits_end = (
                reservation_date.time() <= reservation_end.time() <=
                time(23, 59)
            )

        print("AA opening_time.open_time: ", opening_time.open_time)
        print("AA opening_time.close_time: ", opening_time.close_time)
        print("AA reservation_date.time(): ", reservation_date.time())
        print("AA reservation_end.time(): ", reservation_end.time())
        print("AA reservation_fits_start: ", reservation_fits_start)
        print("AA reservation_fits_end: ", reservation_fits_end)
        print("AA time(23, 59): ", time(23, 59))
        print("XXX: ", opening_time.close_time <= time(23, 59))
        print("XXX: ", opening_time.close_time >= time(4, 00))

        # Raise validation error if the reservation time
        # is before the restaurant opens
        if reservation_date.time() < opening_time.open_time:
            raise forms.ValidationError(
                f"The restaurant is not yet open. Reservations cannot start "
                f"before {opening_time.open_time.strftime('%H:%M')}."
            )

        # Raise validation error if the reservation does not fit
        # within opening hours
        if not reservation_fits_start:
            raise forms.ValidationError(
                f"Reservations must start between "
                f"{opening_time.open_time.strftime('%H:%M')} and "
                f"{opening_time.close_time.strftime('%H:%M')}."
            )

        # Raise validation error if the reservation end time is past 23:59
        if not reservation_fits_end:
            if opening_time.close_time <= time(23, 59):
                raise forms.ValidationError(
                    f"Reservations must finish by closing time "
                    f"{opening_time.close_time.strftime('%H:%M')}. "
                    f"Larger parties require more time."
                )
            else:
                raise forms.ValidationError(
                    f"Reservations must end before midnight. Larger parties "
                    f"require more time."
                )

        # Check if the minutes are a multiple of 15
        if reservation_date.minute % 15 != 0:
            raise forms.ValidationError(
                'Reservation time must be in 15-minute increments.'
            )

        return cleaned_data
