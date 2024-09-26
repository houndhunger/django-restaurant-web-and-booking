from django.test import TestCase
from django.utils import timezone
from booking.forms import ReservationForm, CustomSignupForm
from django.contrib.auth.models import User
from datetime import timedelta


class ReservationFormTest(TestCase):

    def test_reservation_form_is_valid(self):
        data = {
            'reservation_date': timezone.now() + timedelta(days=1, hours=1),  # valid future date
            'guest_count': 5,
            'is_quiet': 'no_preference',
            'is_outside': 'no_preference',
            'has_bench_seating': 'no_preference',
            'has_disabled_access': 'no_preference',
            'note': 'Please prepare a special setup.'
        }
        form = ReservationForm(data=data)
        self.assertTrue(form.is_valid(), msg="Reservation form should be valid")

    def test_reservation_form_is_invalid_guest_count_exceeds_limit(self):
        data = {
            'reservation_date': timezone.now() + timedelta(days=1),
            'guest_count': 15,  # Exceeds max guest count
            'is_quiet': 'no_preference',
            'is_outside': 'no_preference',
            'has_bench_seating': 'no_preference',
            'has_disabled_access': 'no_preference',
            'note': 'Please prepare a special setup.'
        }
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid(), msg="Reservation form should be invalid")
        self.assertIn('guest_count', form.errors)

    def test_reservation_form_is_invalid_date_in_past(self):
        data = {
            'reservation_date': timezone.now() - timedelta(days=1),  # Past date
            'guest_count': 5,
            'is_quiet': 'no_preference',
            'is_outside': 'no_preference',
            'has_bench_seating': 'no_preference',
            'has_disabled_access': 'no_preference',
            'note': 'Please prepare a special setup.'
        }
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid(), msg="Reservation form should be invalid")
        self.assertIn('reservation_date', form.errors)

    def test_signup_form_is_valid(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomSignupForm(data=data)
        self.assertTrue(form.is_valid(), msg="Signup form should be valid")

    def test_signup_form_is_invalid_email_not_unique(self):
        User.objects.create_user(username='johndoe', email='john.doe@example.com', password='testpassword123')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'john.doe@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = CustomSignupForm(data=data)
        self.assertFalse(form.is_valid(), msg="Signup form should be invalid")
        self.assertIn('email', form.errors)
