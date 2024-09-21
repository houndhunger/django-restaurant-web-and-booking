from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

"""
Site Settings model
"""
class SiteSettings(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    contact_email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15, default='0000000000') # Assuming a 15-character limit for the phone number
    def __str__(self):
        return f"{self.site.domain} Settings"

"""
Table model
"""
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    zone = models.IntegerField()
    capacity = models.IntegerField()
    vip_category = models.IntegerField(choices=[(1, 'Standard'), (2, 'Premium'), (3, 'VIP')])
    is_quiet = models.BooleanField(default=False)
    is_outside = models.BooleanField(default=False)
    has_bench_seating = models.BooleanField(default=False)
    has_disabled_access = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True, null=True)
    adjacent_tables = models.ManyToManyField('self', blank=True, symmetrical=True)  # Removed related_name

    def __str__(self):
        return f"Table {self.table_number} (Zone {self.zone})"

# Reservation status choices
RESERVATION_STATUS_CHOICES = (
    (0, "Pending"),
    (1, "Confirmed"),
    (2, "Cancelled"),
    (3, "Deleted"),
)

"""
Reservation model
"""
class Reservation(models.Model):
    PREFERENCE_CHOICES = [
        ('no_preference', 'No Preference'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    is_quiet = models.CharField(max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    is_outside = models.CharField(max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    has_bench_seating = models.CharField(max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')
    has_disabled_access = models.CharField(max_length=20, choices=PREFERENCE_CHOICES, default='no_preference')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_count = models.PositiveIntegerField()
    reservation_date = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=2))
    #reservation_end = models.DateTimeField(editable=False, null=True)
    tables = models.ManyToManyField(Table)  # Multiple tables can be reserved for one reservation
    note = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=RESERVATION_STATUS_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set', on_delete=models.SET_NULL, null=True, editable=False)
    edited_by = models.ForeignKey(User, related_name='edited_%(class)s_set', on_delete=models.SET_NULL, null=True, editable=False)

    def save(self, *args, **kwargs):
        # if not self.pk:  # Check if the object is being created
        #     self.reservation_end = self.reservation_date + self.duration
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]

    # @property
    # def reservation_end(self):
    #     """Calculate the end time of the reservation."""
    #     return getattr(self, '_reservation_end', self.reservation_date + self.duration)  # Ensure you define 'duration' in your form or model

    def is_conflicting(self, new_reservation):
        """
        Check if the new reservation conflicts with this reservation.
        """
        new_end_time = new_reservation.reservation_date + new_reservation.duration
        return (self.reservation_date < new_end_time) and (self.reservation_end > new_reservation.reservation_date)

    @staticmethod
    def check_table_availability(tables, start_time, end_time):
        """
        # Check if any of the given tables are available for the specified time range.
        """
        overlapping_reservations = Reservation.objects.filter(
            tables__in=tables,
            reservation_date__lt=end_time,
            reservation_end__gt=start_time,
            status='confirmed'
        ).exists()
        return not overlapping_reservations

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.reservation_date}"
