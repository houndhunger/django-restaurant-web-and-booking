from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Reservation, Table
from .forms import ReservationForm
from datetime import timedelta

# # Create your views here.
# class PostList(generic.ListView):
#     model = Reservation
#     queryset = Reservation.objects.all()
#     # template_name = "reservation_list.html"
#     #queryset = Reservation.objects.filter(status=1)
#     template_name = "booking/index.html"
#     paginate_by = 6


# Home view...
class HomeView(TemplateView):
    template_name = 'booking/index.html'

def restaurant_menu(request):
    return render(request, 'restaurant/restaurant_menu.html')


# View to display restaurant menu
class RestaurantMenuView(TemplateView):
    template_name = 'restaurant/restaurant_menu.html'

def restaurant_menu(request):
    return render(request, 'restaurant/restaurant_menu.html')


# View to list all reservations (not guest)
class ManageReservationsView(UserPassesTestMixin, generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    template_name = "booking/reservations_list.html"
    paginate_by = 6

    def test_func(self):
        # Ensure that the user is staff
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Optionally redirect non-staff users to another page
        from django.shortcuts import redirect
        return redirect('home')


# View to list all tables (not guest)
class ManageTablesView(UserPassesTestMixin, generic.ListView):
    model = Table
    queryset = Reservation.objects.all()
    template_name = "booking/tables_list.html"
    paginate_by = 12

    def test_func(self):
        # Ensure that the user is staff
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Optionally redirect non-staff users to another page
        from django.shortcuts import redirect
        return redirect('home')


# View to list the reservations for the currently logged-in user
class UserReservationsView(generic.ListView):
    model = Reservation
    template_name = 'booking/user_reservations.html'
    paginate_by = 6

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


# # View to make a new reservation
# class MakeReservationView(TemplateView):
#     template_name = 'booking/reservation_make.html'

#     def get(self, request, *args, **kwargs):
#         form = ReservationForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user  # Associate the logged-in user
#             reservation.save()
#             return redirect(reverse('user_reservations'))
#         return render(request, self.template_name, {'form': form})


# # View to make a new reservation
class MakeReservationView(TemplateView):
    template_name = 'booking/reservation_make.html'

    def get(self, request, *args, **kwargs):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Associate the logged-in user

            # Get reservation details
            reservation_date = reservation.reservation_date
            reservation_end = reservation_date + timedelta(hours=2)  # Default 2-hour duration

            # Calculate total tables and reserved tables
            total_tables = Table.objects.count()
            reserved_tables_count = Reservation.objects.filter(
                reservation_date__date=reservation_date.date(),
                status=1
            ).count()

            # Determine if the restaurant is more than half full
            half_full = reserved_tables_count >= total_tables / 2

            # Extract preferences from the form
            quiet = form.cleaned_data.get('quiet')
            outside = form.cleaned_data.get('outside')
            bench_seating = form.cleaned_data.get('bench_seating')
            disabled_access = form.cleaned_data.get('disabled_access')

            # Filter tables based on preferences
            tables = Table.objects.filter(
                is_quiet=quiet,
                is_outside=outside,
                has_bench_seating=bench_seating,
                has_disabled_access=disabled_access,
            )

            # Apply odd/even logic based on reservation date
            if half_full:
                available_tables = tables
            else:
                # Apply odd/even logic based on the reservation date
                if reservation_date.day % 2 == 0:
                    available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 == 0])
                else:
                    available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 != 0])

            # Check for available tables within the filtered set
            available_tables = available_tables.filter(
                ~Q(reservation__reservation_date__lt=reservation.reservation_end) &
                ~Q(reservation__reservation_end__gt=reservation.reservation_date)
            ).distinct()

            # Assign tables if available
            if available_tables.exists():
                reservation.save()
                reservation.tables.set(available_tables[:reservation.guest_count])  # Assign tables based on guest count
                return redirect(reverse('user_reservations'))
            else:
                # Return form with error if no tables are available
                form.add_error(None, 'No available tables for the selected date and preferences.')

        return render(request, self.template_name, {'form': form})


# View to edit reservation
class EditReservationView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_edit.html'
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