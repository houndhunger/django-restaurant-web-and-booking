from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RESERVATION_STATUS_CHOICES = (
    (0, "Pending"), # add settings for resturant booking - reservation_auto_approve T/F
    (1, "Confirmed"),
    (2, "Cancelled"),
)

# Reservation model
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    guest_count = models.IntegerField()
    # tables = models.ManyToManyField(Table, related_name='reservations') # TablesId (List of FK)
    # 
    # on_delete=models.CASCADE - not good idea, table deletion 
    # sholud be allowed only if there are no reservations related to it. 
    # First all related reservations sholud moved to different tables.
    note = models.TextField(blank=True, null=True)  # Note
    status = models.IntegerField(choices=RESERVATION_STATUS_CHOICES, default=0) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    #created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reservations')
    #edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_reservations')

    created_by = models.ForeignKey(User, related_name='created_%(class)s_set', on_delete=models.SET_NULL, null=True, editable=False)
    edited_by = models.ForeignKey(User, related_name='edited_%(class)s_set', on_delete=models.SET_NULL, null=True, editable=False)

    # reservation can have payment related to it payment("Pending","Received","Cancelled")

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is new (being created)
            self.created_by = kwargs.pop('user', None)
        self.edited_by = kwargs.pop('user', None)
        super(Reservation, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.reservation_date}"