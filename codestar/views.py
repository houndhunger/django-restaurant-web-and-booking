from django.shortcuts import render
from django.views.generic import TemplateView

"""
View to welcome which is now home - index.html
"""
def welcome_view(request):
    return render(request, 'index.html')

"""
Home view - index.html
"""
class HomeView(TemplateView):
    template_name = 'index.html'

"""
View to display restaurant menu
"""
class RestaurantMenuView(TemplateView):
    template_name = 'restaurant/restaurant_menu.html'

# def restaurant_menu(request):
#     return render(request, 'restaurant/restaurant_menu.html')
