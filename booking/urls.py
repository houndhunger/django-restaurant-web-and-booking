from . import views
from django.urls import path
from .views import BookingCreateView, BookingListView

urlpatterns = [
    path('booking/', views.PostList.as_view(), name='home'),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('list/', BookingListView.as_view(), name='booking_list'),
]