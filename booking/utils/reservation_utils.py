from django.db.models import Q
from booking.models import Table, Reservation  # Use absolute imports
from datetime import timedelta

def handle_reservation_logic(form, user):
    reservation = form.save(commit=False)
    reservation.user = user

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

    # Determine if the restaurant is more than half full
    total_tables = Table.objects.count()
    reserved_tables_count = Reservation.objects.filter(
        reservation_date__date=reservation_date.date(),
        status=1
    ).count()
    half_full = reserved_tables_count >= total_tables / 2

    if half_full:
        available_tables = tables
    else:
        if reservation_date.day % 2 == 0:
            available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 == 0])
        else:
            available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 != 0])

    # Check for overlapping reservations
    overlapping_reservations = Reservation.objects.filter(
        Q(reservation_date__lt=reservation_end) &
        Q(reservation_date__gt=reservation_date - timedelta(hours=2))
    )
    reserved_table_ids = overlapping_reservations.values_list('tables', flat=True)

    available_tables = available_tables.exclude(pk__in=reserved_table_ids)

    return reservation, available_tables
