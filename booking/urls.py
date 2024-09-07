from . import views
from django.urls import path
from .views import (
    HomeView,
    UserReservationsView,
    MakeReservationView,
    PreviewReservationView,
    EditReservationView,   
    DeleteReservationView
)

urlpatterns = [
    path('menu/', HomeView.as_view(), name='home'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('make-reservation/', MakeReservationView.as_view(), name='make_reservation'),
    path('preview-reservation/<int:pk>/', PreviewReservationView.as_view(), name='preview_reservation'),
    #path('edit-reservation/<int:pk>/', EditReservationView.as_view(), name='edit_reservation'),
    path('delete-reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete_reservation'),
]