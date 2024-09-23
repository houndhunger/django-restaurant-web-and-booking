from . import views
from django.urls import path, include

from .views import check_email_unique

from .views import (
    UserReservationsView,
    MakeReservationView,
    EditReservationView,
    ReservationPreviewView,
    DeleteReservationView,
    CustomSignupView,
)

urlpatterns = [
    path(
        'check-email-unique/', check_email_unique,
        name='check_email_unique'
    ),
    path(
        'reservations/', UserReservationsView.as_view(),
        name='user_reservations'
    ),
    path(
        'reservation/make/', MakeReservationView.as_view(),
        name='make_reservation'
    ),
    path(
        'reservation/<int:pk>/edit/', EditReservationView.as_view(),
        name='edit_reservation'
    ),
    path(
        'reservation/<int:pk>/preview/', ReservationPreviewView.as_view(),
        name='preview_reservation'
    ),
    path(
        'delete-reservation/<int:pk>/', DeleteReservationView.as_view(),
        name='delete_reservation'
    ),
]
