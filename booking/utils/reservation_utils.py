from django import forms
from django.db.models import Q
from booking.models import Table, Reservation  # Use absolute imports
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


"""
Handles reservation logic
"""
def handle_reservation_logic(form, user, original_reservation):
    reservation = form.save(commit=False)
    reservation.user = user
    reservation.status = 1  # Set status to 'Confirmed'

    reservation_date = reservation.reservation_date
    reservation_end = reservation_date + timedelta(hours=2)

    preferences = {
        'is_quiet': form.cleaned_data.get('is_quiet') == 'yes',
        'is_outside': form.cleaned_data.get('is_outside') == 'yes',
        'has_bench_seating': form.cleaned_data.get('has_bench_seating') == 'yes',
        'has_disabled_access': form.cleaned_data.get('has_disabled_access') == 'yes'
    }

    # Start with all tables and filter based on preferences
    tables = Table.objects.all()
    for key, value in preferences.items():
        if value:
            tables = tables.filter(**{key: True})

    # Find overlapping reservations considering a 2-hour overlap
    overlapping_reservations = Reservation.objects.filter(
        Q(reservation_date__lt=reservation_end) &
        Q(reservation_date__gt=reservation_date - timedelta(hours=2)) &
        Q(status=1)  # Only consider confirmed reservations
    ).values_list('tables', flat=True)

    print(f"overlapping_reservations: {list(overlapping_reservations)}")  # Convert to list for easier viewing

    # Exclude already booked tables from available tables
    available_tables = tables.exclude(pk__in=overlapping_reservations)
    # Initialize assigned_tables
    assigned_tables = []
    # Create a dictionary to track available capacity by zone
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
        raise forms.ValidationError("Not enough available tables for the selected date and preferences.")

    # Save the reservation and assign tables
    reservation.save()
    reservation.tables.set(assigned_tables)

    print(f"assigned_tables: {assigned_tables}")

    print(f"AAA reservation id: {reservation.id}")
    print(f"AAA reservation date: {reservation.reservation_date}")
    print(f"AAA reservation status: {reservation.status}")
    print(f"AAA reservation guest_count: {reservation.guest_count}")
    print(f"AAA reservation tables: {reservation.tables.all()}")  # This will list associated tables

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