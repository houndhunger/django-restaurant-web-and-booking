from django import forms
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import timedelta
from booking.models import Table, Reservation, OpeningTime, ReservationTimeSpan


def handle_reservation_logic(form, user, original_reservation=None):
    """
    Handles reservation logic, including table assignment and email sending.
    """
    reservation = form.save(commit=False)
    reservation.user = user
    reservation.status = 1  # Set status to 'Confirmed'

    # Get preferences from the form
    preferences = {
        'is_quiet': form.cleaned_data.get('is_quiet'),
        'is_outside': form.cleaned_data.get('is_outside'),
        'has_bench_seating': form.cleaned_data.get('has_bench_seating'),
        'has_disabled_access': form.cleaned_data.get('has_disabled_access')
    }

    tables = Table.objects.all()
    for key, value in preferences.items():
        if value == 'yes':
            tables = tables.filter(**{key: True})
        elif value == 'no':
            tables = tables.filter(**{key: False})

    overlapping_reservations = Reservation.objects.none()

    # Exclude already booked tables from available tables
    overlapping_tables = overlapping_reservations.values_list(
        'tables', flat=True
    )
    available_tables = tables.exclude(pk__in=overlapping_tables)

    assigned_tables = []
    remaining_guests = reservation.guest_count

    # Assign tables within the same zone (optimizing for capacity)
    zone_capacity = {}
    for table in available_tables:
        if table.zone not in zone_capacity:
            zone_capacity[table.zone] = 0
        zone_capacity[table.zone] += table.capacity

    # Check if zone_capacity is empty
    if not zone_capacity:
        form.add_error(None, "No available tables match your preferences.")
        return None, None

    # Select the zone with the most available capacity
    optimal_zone = max(zone_capacity, key=zone_capacity.get)

    zone_tables = available_tables.filter(zone=optimal_zone)

    for table in zone_tables:
        if remaining_guests <= 0:
            break
        if table.capacity >= remaining_guests:
            assigned_tables.append(table)
            remaining_guests = 0
        else:
            assigned_tables.append(table)
            remaining_guests -= table.capacity

    if remaining_guests > 0:
        form.add_error(
            None, "Not enough available tables for the date and preferences."
        )
        return None, None

    # Save reservation and assign tables
    reservation.save()
    reservation.tables.set(assigned_tables)

    # Send confirmation email
    email_subject = 'Reservation Confirmation'
    email_body = render_to_string(
        'account/email/reservation_confirmation_email.txt', {
            'user': user, 'reservation': reservation,
        }
    )
    send_mail(
        email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email]
    )

    return reservation, assigned_tables


@csrf_exempt
def check_email_unique(request):
    """
    Check email
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        is_unique = not User.objects.filter(email=email).exists()
        return JsonResponse({'is_unique': is_unique})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def format_duration(duration: timedelta) -> str:
    """
    Convert a timedelta duration into a readable format
    like '2 hours and 15 minutes'.
    """
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return ' and '.join(parts) if parts else "0 minutes"
