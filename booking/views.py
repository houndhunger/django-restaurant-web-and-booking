from django.shortcuts import render
# from django.http import HttpResponse
from django.views import generic
from .models import Reservation

# Create your views here.
# def my_booking(request):
#     return HttpResponse("Hello, Booking!")

# Create your views here.
class PostList(generic.ListView):
    model = Reservation