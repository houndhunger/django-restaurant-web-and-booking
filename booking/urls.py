from . import views
from django.urls import path, include

from .views import check_email_unique
from booking.utils.reservation_utils import get_available_tables

from .views import (
    UserReservationsView,
    MakeReservationView,
    EditReservationView,
    ReservationPreviewView, 
    DeleteReservationView,
    ManageReservationsView,
    ManageTablesView,
    CustomSignupView,
)

urlpatterns = [
    path('check-email-unique/', check_email_unique, name='check_email_unique'),
    #path('menu/', RestaurantMenuView.as_view(), name='restaurant_menu'),
    
    # staf manage urls
    path('manage-reservations/', ManageReservationsView.as_view(), name='manage_reservations'),
    path('manage-tables/', ManageTablesView.as_view(), name='manage_tables'),

    # guest reservations
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('reservation/make/', MakeReservationView.as_view(), name='make_reservation'), 
    path('reservation/<int:pk>/edit/', EditReservationView.as_view(), name='edit_reservation'),
    path('reservation/<int:pk>/preview/', ReservationPreviewView.as_view(), name='preview_reservation'),
    path('delete-reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete_reservation'),

    #AJAX - WIP
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('get-available-tables/', get_available_tables, name='get_available_tables'),
]
