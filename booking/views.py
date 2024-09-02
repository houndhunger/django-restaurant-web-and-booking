from django.shortcuts import render
# from django.http import HttpResponse
from django.views import generic
from .models import Reservation
from django.views.generic import TemplateView

# Create your views here.
# def my_booking(request):
#     return HttpResponse("Hello, Booking!")

# Create your views here.
class PostList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    # template_name = "reservation_list.html"
    #queryset = Reservation.objects.filter(status=1)
    template_name = "booking/index.html"
    paginate_by = 6

class HomePageView(TemplateView):
    template_name = "booking/index.html"

class BookingCreateView(TemplateView):
    template_name = "booking/index.html"

class BookingListView(TemplateView):
    template_name = "booking/index.html"