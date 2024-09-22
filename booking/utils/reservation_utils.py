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


"""
Handles reservation logic
"""
def handle_reservation_logic(form, user, original_reservation):
    reservation = form.save(commit=False)
    reservation.user = user
    reservation.status = 1  # Set status to 'Confirmed'

    reservation_date = reservation.reservation_date

    # Ensure guest_count is defined from the reservation
    guest_count = reservation.guest_count

    try:
        time_span = ReservationTimeSpan.objects.get(guest_count=guest_count)
        reservation_end = reservation_date + time_span.duration  # Use the duration from ReservationTimeSpan
        reservation.reservation_end_date = reservation_end
    except ReservationTimeSpan.DoesNotExist:
        form.add_error(None, 'Please contact the restaurant for large party sizes.')
        return None, None  # Return early to display the form error

    # Get the reservation day as abbreviation
    reservation_day = reservation.reservation_date.strftime('%a').lower()  
    opening_time = OpeningTime.objects.filter(day_of_week=reservation_day).first()

    if not opening_time or not (opening_time.open_time <= reservation_date.time() <= opening_time.close_time):
        form.add_error(None, 'The restaurant is closed at the time of your reservation.')
        return None, None  # Return early to display the form error

    preferences = {
        'is_quiet': form.cleaned_data.get('is_quiet'),
        'is_outside': form.cleaned_data.get('is_outside'),
        'has_bench_seating': form.cleaned_data.get('has_bench_seating'),
        'has_disabled_access': form.cleaned_data.get('has_disabled_access')
    }

    # Start with all tables and filter based on preferences
    tables = Table.objects.all()
    for key, value in preferences.items():
        if value == 'yes':
            tables = tables.filter(**{key: True})
        elif value == 'no':
            tables = tables.filter(**{key: False})

    # #
    # # ALLOW overlapping by using an empty queryset
    # overlapping_reservations = Reservation.objects.none() 
    # #
    """
    Comment out above and uncommet bellow to FORBID overlapping reservations
    Uncommet above and comment out bellow to ALLOW overlapping reservations

    """
    # #
    # FORBID Find overlapping reservations considering a 2-hour overlap
    overlapping_reservations = Reservation.objects.filter(
        Q(reservation_date__lt=reservation_end) & 
        Q(reservation_date__gt=reservation_date - timedelta(hours=2)) & 
        Q(user=user) & 
        Q(status=1)  # Only consider confirmed reservations
    ).exclude(pk=original_reservation.pk if original_reservation else None)
    # #

    if overlapping_reservations.exists():
        form.add_error(None, 'You already have an overlapping reservation for this time. '
                             'Please, for larger groups, contact the restaurant staff directly.')
        return None, None  # Return early to display the form error

    # Exclude already booked tables from available tables
    overlapping_tables = overlapping_reservations.values_list('tables', flat=True)
    available_tables = tables.exclude(pk__in=overlapping_tables)

    # Initialize assigned_tables and create a dictionary to track available capacity by zone
    assigned_tables = []
    zone_capacity = {}

    # If editing an existing reservation, include original assigned tables
    if original_reservation:
        original_tables = original_reservation.tables.all()
        original_table_ids = original_tables.values_list('pk', flat=True)

        # Re-add original tables to available tables pool
        available_tables = available_tables | original_tables

        # Add original tables' guest count to their corresponding zone
        for table in original_tables:
            if table.zone in zone_capacity:
                zone_capacity[table.zone] += table.capacity
            else:
                zone_capacity[table.zone] = table.capacity

        # Add original tables to assigned_tables
        assigned_tables.extend(original_tables)

        # Update the remaining guest count based on already assigned tables
        if assigned_tables:
            total_capacity_assigned = sum(table.capacity for table in assigned_tables)
            remaining_guests = max(0, reservation.guest_count - total_capacity_assigned)
        else:
            remaining_guests = reservation.guest_count
    else:
        remaining_guests = reservation.guest_count

    # Calculate available capacity for each zone (including original reservation's tables)
    for table in available_tables:
        if table.zone not in zone_capacity:
            zone_capacity[table.zone] = 0
        zone_capacity[table.zone] += table.capacity

    # Select the zone with the most available capacity
    if zone_capacity:
        optimal_zone = max(zone_capacity, key=zone_capacity.get)
        # Filter available tables within the selected zone
        zone_tables = available_tables.filter(zone=optimal_zone)

        # Assign additional tables within the optimal zone
        for table in zone_tables:
            if remaining_guests <= 0:
                break
            if table.capacity >= remaining_guests:
                assigned_tables.append(table)
                remaining_guests = 0  # All guests are seated
            else:
                assigned_tables.append(table)
                remaining_guests -= table.capacity  # Reduce remaining guest count

    # If guests remain unseated after checking all available tables
    if remaining_guests > 0:
        form.add_error(None, "Not enough available tables for the selected date and preferences.")
        return None, None  # Return early to display the form error

    # Save the reservation and assign tables
    reservation.save()
    reservation.tables.set(assigned_tables)

    # Send confirmation email
    email_subject = 'Reservation Confirmation'
    email_body = render_to_string('account/email/reservation_confirmation_email.txt', {
        'user': user,
        'reservation': reservation,
    })

    send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return reservation, assigned_tables


"""
Check email
"""
@csrf_exempt
def check_email_unique(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        is_unique = not User.objects.filter(email=email).exists()
        return JsonResponse({'is_unique': is_unique})
    return JsonResponse({'error': 'Invalid request'}, status=400)