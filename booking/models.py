from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RESERVATION_STATUS_CHOICES = (
    (0, "Pending"),
    (1, "Confirmed"),
    (2, "Cancelled"),
)

# Reservation model
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    guest_count = models.IntegerField()
    # table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.IntegerField(choices=RESERVATION_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.reservation_date}"