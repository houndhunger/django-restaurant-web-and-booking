from . import views
from django.urls import path, include
from .views import (
    HomeView,
    RestaurantMenuView,
    UserReservationsView,
    MakeReservationView,
    #EditReservationView,   
    DeleteReservationView,
    ManageReservationsView,
    ManageTablesView,
    #SignUpView,
    CustomSignupView,
    #LogInView,
    #CustomLoginView,
    #signup_view
    ReservationUpdateView,

)

urlpatterns = [
    path('menu/', RestaurantMenuView.as_view(), name='restaurant_menu'),
    path('reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('manage-reservations/', ManageReservationsView.as_view(), name='manage_reservations'),
    path('manage-tables/', ManageTablesView.as_view(), name='manage_tables'),
    
    #path('make-reservation/', MakeReservationView.as_view(), name='make_reservation'),

    # path('reserve/', ReservationCreateUpdateView.as_view(), name='make_reservation'),  # For creating
    # path('reserve/edit/<int:pk>/', ReservationCreateUpdateView.as_view(), name='edit_reservation'),  # For editing

    path('reserve/', MakeReservationView.as_view(), name='make_reservation'),
    path('reserve/<int:pk>/edit/', ReservationUpdateView.as_view(), name='edit_reservation'),


    #path('preview-reservation/', PreviewReservationView.as_view(), name='preview_reservation'),
    
    #path('edit-reservation/<int:pk>/', EditReservationView.as_view(), name='edit_reservation'),
    
    path('delete-reservation/<int:pk>/', DeleteReservationView.as_view(), name='delete_reservation'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    #path('login/', CustomLoginView.as_view(), name='login'),
    #path('accounts/signup/', signup_view, name='account_signup'),
    #path('accounts/login/', login_view, name='account_login'),
]
