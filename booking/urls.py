from . import views
from django.urls import path
from .views import (
    HomeView,
    RestaurantMenuView,
    UserReservationsView,
    MakeReservationView,
    EditReservationView,   
    DeleteReservationView,
    ManageReservationsView,
    ManageTablesView
)

urlpatterns = [
    path('menu/', RestaurantMenuView.as_view(), name='restaurant_menu'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('manage-reservations/', ManageReservationsView.as_view(), name='manage_reservations'),
    path('manage-tables/', ManageTablesView.as_view(), name='manage_tables'),
    path('make-reservation/', MakeReservationView.as_view(), name='make_reservation'),
    #path('preview-reservation/', PreviewReservationView.as_view(), name='preview_reservation'),
    path('edit-reservation/<int:pk>/', EditReservationView.as_view(), name='edit_reservation'),
    path('delete-reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete_reservation'),
]