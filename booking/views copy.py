from django.shortcuts import render
# from django.http import HttpResponse
from django.views import generic
from .models import Reservation
from django.views.generic import TemplateView

# Create your views here.
class PostList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    # template_name = "reservation_list.html"
    #queryset = Reservation.objects.filter(status=1)
    template_name = "booking/index.html"
    paginate_by = 6

# class HomePageView(TemplateView):
#     template_name = "booking/index.html"

class HomeView(TemplateView):
    template_name = 'restaurant/restaurant_menu.html'

def restaurant_menu(request):
    return render(request, 'restaurant/restaurant_menu.html')

class RestaurantMenuView(TemplateView):
    template_name = 'restaurant_menu.html'

class UserReservationsView(TemplateView):
    template_name = 'user_reservations.html'

class CreateReservationView(TemplateView):
    # Implement your booking creation logic
    pass

# class BookingListView(TemplateView):
#     # Implement your booking listing logic
#     pass
