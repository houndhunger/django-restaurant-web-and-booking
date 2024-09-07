from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reservation
from .forms import ReservationForm

# Create your views here.
class PostList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    # template_name = "reservation_list.html"
    #queryset = Reservation.objects.filter(status=1)
    template_name = "booking/index.html"
    paginate_by = 6

# Home view to display restaurant menu
class HomeView(TemplateView):
    template_name = 'restaurant/restaurant_menu.html'

def restaurant_menu(request):
    return render(request, 'restaurant/restaurant_menu.html')

# View to list all reservations (admin view, for example)
class ReservationListView(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    template_name = "booking/reservation_list.html"
    paginate_by = 6

# View to list the reservations for the currently logged-in user
class UserReservationsView(generic.ListView):
    model = Reservation
    template_name = 'booking/user_reservations.html'
    paginate_by = 6

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

# View to review a single reservation
# class ReviewReservationView(DetailView):
#     model = Reservation
#     template_name = 'booking/reservation_preview.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reservation'] = get_object_or_404(Reservation, id=self.kwargs['pk'])
#         return context

# View to make a new reservation
class MakeReservationView(TemplateView):
    template_name = 'booking/reservation_make.html'

    def get(self, request, *args, **kwargs):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect(reverse('preview_reservation', kwargs={'pk': reservation.pk}))
        return render(request, self.template_name, {'form': form})

# View to preview a reservation before confirmation (you can use this before actual submission)
class PreviewReservationView(TemplateView):
    template_name = 'booking/reservation_preview.html'
    context_object_name = 'reservation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['reservation'] = Reservation.objects.get(pk=pk)
        return context

    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Process the reservation as needed (e.g., save it to the database)
            reservation.save()
            context = {'form': form, 'reservation': reservation}
            return render(request, self.template_name, context)
        # If the form is invalid, re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form))

# View to edit reservation
class EditReservationView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'edit_reservation.html'
    success_url = reverse_lazy('user_reservations')  # Redirect after successful update

    def get_object(self, queryset=None):
        # Ensure that the object being edited is the one in the URL
        return super().get_object(queryset)

# View to delete a reservation
class DeleteReservationView(DeleteView):
    model = Reservation
    template_name = 'booking/reservation_delete.html'
    success_url = reverse_lazy('user_reservations')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, id=self.kwargs['pk'], user=self.request.user)