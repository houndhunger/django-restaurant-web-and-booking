from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
#from .models import SiteSettings
from booking.models import SiteSettings

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSettings.objects.first()  # Ensure the site settings exist
        context['site_settings'] = site_settings
        return context

"""
View to display restaurant menu
"""
class RestaurantMenuView(TemplateView):
    template_name = 'restaurant/restaurant_menu.html'

# def restaurant_menu(request):
#     return render(request, 'restaurant/restaurant_menu.html')

def contact(request):
    site_settings = SiteSettings.objects.first()

    if not site_settings:
        return HttpResponse("Site settings are not configured.")

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Prepare the message
        full_message = f"From Dino Restaurant Booking System:\n\nMessage from {first_name} {last_name}, Email: {email}\n\n{message}"
        
        # Send the email
        send_mail(
            'Contact Form Submission',
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ['daniel.pribula@gmail.com'],  # Your email address
        )
        
        return HttpResponse('Thank you for your message!')

    return render(request, 'restaurant/contact.html', {
        'site_settings': site_settings,
    })
