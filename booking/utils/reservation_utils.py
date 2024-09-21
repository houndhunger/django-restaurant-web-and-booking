from django.db.models import Q
from booking.models import Table, Reservation  # Use absolute imports
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


"""
Handels reservation logic
"""
def handle_reservation_logic(form, user):
    print("reservation logic")
    reservation = form.save(commit=False)
    reservation.user = user

    # Set the reservation status to 'Confirmed'
    # reservation can beset to 'Pending' manually by staff
    reservation.status = 1  # Set status to 'Confirmed'

    # Reservation end time calculation
    reservation_date = reservation.reservation_date
    reservation_end = reservation_date + timedelta(hours=2)

    # Table preferences
    is_quiet = form.cleaned_data.get('is_quiet')
    is_outside = form.cleaned_data.get('is_outside')
    has_bench_seating = form.cleaned_data.get('has_bench_seating')
    has_disabled_access = form.cleaned_data.get('has_disabled_access')

    # Filter tables based on preferences
    tables = Table.objects.all()
    preferences = {
        'is_quiet': is_quiet,
        'is_outside': is_outside,
        'has_bench_seating': has_bench_seating,
        'has_disabled_access': has_disabled_access
    }
    for key, value in preferences.items():
        if value == 'yes':
            tables = tables.filter(**{key: True})
        elif value == 'no':
            tables = tables.filter(**{key: False})


    # Find IDs of tables that are already booked during the desired time
    overlapping_reservations = Reservation.objects.filter(
        reservation_date__lt=reservation_end,
        reservation_date__gt=reservation_date,
        status=1  # Only consider confirmed reservations
    ).values_list('tables', flat=True)

    # Exclude already booked tables from available tables
    available_tables = tables.exclude(pk__in=overlapping_reservations)

    # If there aren't enough available tables, raise an error
    if available_tables.count() < reservation.guest_count:
        raise forms.ValidationError("Not enough available tables for the selected date and preferences.")

    print(f"available_tables.count():{available_tables.count()}")

    # Select tables based on the guest count
    assigned_tables = available_tables[:reservation.guest_count]

    # # Determine if the restaurant is more than half full
    # total_tables = Table.objects.count()
    # reserved_tables_count = Reservation.objects.filter(
    #     reservation_date__date=reservation_date.date(),
    #     status=1
    # ).count()
    # half_full = reserved_tables_count >= total_tables / 2

    # if half_full:
    #     available_tables = tables
    # else:
    #     if reservation_date.day % 2 == 0:
    #         available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 == 0])
    #     else:
    #         available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 != 0])

    # Check for overlapping reservations
    # overlapping_reservations = Reservation.objects.filter(
    #     Q(reservation_date__lt=reservation_end) &
    #     Q(reservation_date__gt=reservation_date - timedelta(hours=2))
    # ).exclude(pk=reservation.pk)  # Exclude the current reservation

    #reserved_table_ids = overlapping_reservations.values_list('tables', flat=True)

    #available_tables = available_tables.exclude(pk__in=reserved_table_ids)

    return reservation, available_tables


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

    # In reservation_utils.py


"""
Get avaialable tables
"""
@csrf_exempt
def get_available_tables(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')

            if date:
                # Your logic to fetch available tables based on the date
                available_tables = Table.objects.filter(reservation_date=date)
                tables_list = [{'number': table.number} for table in available_tables]
                return JsonResponse({'tables': tables_list})
            
            return JsonResponse({'error': 'Date is required'}, status=400)
        except Exception as e:
            #print(f"Error: {e}")  # Log the error
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)