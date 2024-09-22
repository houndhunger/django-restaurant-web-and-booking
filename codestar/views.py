from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from booking.models import SiteSettings, OpeningTime

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


class OpeningTimesView(ListView):
    model = OpeningTime
    template_name = 'restaurant/opening_times.html'
    context_object_name = 'opening_times'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opening_times'] = self.get_queryset()
        context['show_opening_time_table'] = True  # Control table visibility
        context['loaded_through_opening_times'] = True  # Control sumary visibility - details and sumary will be hidden
        return context

    def get_queryset(self):
        return OpeningTime.objects.all().order_by('day_of_week')