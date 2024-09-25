from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class SiteSettings(models.Model):
    """
    Site Settings model
    """
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    contact_email = models.EmailField(max_length=254)
    # Assuming a 15-character limit for the phone number
    phone_number = models.CharField(max_length=15, default='0000000000')

    class Meta:
        verbose_name_plural = "Site Settings"  # Plural name

    def __str__(self):
        return f"{self.site.domain} Settings"


DAYS_OF_WEEK = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
]


class OpeningTime(models.Model):
    """
    Opening Time model
    """
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        verbose_name = 'Opening Time'
        verbose_name_plural = 'Opening Times'
        ordering = ['day_of_week']

    def __str__(self):
        return f"{self.day_of_week}: {self.open_time} - {self.close_time}"


class ReservationTimeSpan(models.Model):
    """
    Reservation Time Span model
    """
    guest_count = models.PositiveIntegerField()  # Size of the party
    duration = models.DurationField()  # Duration of the reservation

    def __str__(self):
        return f"Party Size: {self.guest_count}, Duration: {self.duration}"


class Table(models.Model):
    """
    Table model
    """
    table_number = models.IntegerField(unique=True)
    zone = models.IntegerField()
    capacity = models.IntegerField()
    vip_category = models.IntegerField(choices=[
        (1, 'Standard'), (2, 'Premium'), (3, 'VIP')
    ])
    is_quiet = models.BooleanField(default=False)
    is_outside = models.BooleanField(default=False)
    has_bench_seating = models.BooleanField(default=False)
    has_disabled_access = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True, null=True)
    adjacent_tables = models.ManyToManyField(
        'self', blank=True, symmetrical=True
    )

    def __str__(self):
        return f"Table {self.table_number} (Zone {self.zone})"


# Reservation status choices
RESERVATION_STATUS_CHOICES = (
    (0, "Pending"),
    (1, "Confirmed"),
    (2, "Cancelled"),
    (3, "Deleted"),
)


class Reservation(models.Model):
    """
    Reservation model
    """
    PREFERENCE_CHOICES = [
        ('no_preference', 'No Preference'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    is_quiet = models.CharField(
        max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    is_outside = models.CharField(
        max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    has_bench_seating = models.CharField(
        max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    has_disabled_access = models.CharField(
        max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_count = models.PositiveIntegerField()
    reservation_date = models.DateTimeField()
    reservation_end_date = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta(hours=2))
    tables = models.ManyToManyField(Table)
    note = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=RESERVATION_STATUS_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='created_%(class)s_set', on_delete=models.SET_NULL,
        null=True, editable=False
    )
    edited_by = models.ForeignKey(
        User, related_name='edited_%(class)s_set', on_delete=models.SET_NULL,
        null=True, editable=False
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]

    def is_conflicting(self, new_reservation):
        # Check if the new reservation conflicts with this reservation
        new_end_time = (
            new_reservation.reservation_date +
            new_reservation.duration
        )
        + new_reservation.duration
        return (
            self.reservation_date < new_end_time) and (
            self.reservation_end > new_reservation.reservation_date)

    @staticmethod
    def check_table_availability(tables, start_time, end_time):
        # Check if any of the tables are available for the specified time range
        overlapping_reservations = Reservation.objects.filter(
            tables__in=tables,
            reservation_date__lt=end_time,
            reservation_end__gt=start_time,
            status='confirmed'
        ).exists()
        return not overlapping_reservations

    def __str__(self):
        return f"Reservation by {self.user.username}"
        "on {self.reservation_date}"
