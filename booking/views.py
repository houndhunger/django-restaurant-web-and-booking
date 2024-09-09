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


# View to make a new reservation
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
            is_quiet = form.cleaned_data.get('is_quiet')
            is_outside = form.cleaned_data.get('is_outside')
            has_bench_seating = form.cleaned_data.get('has_bench_seating')
            has_disabled_access = form.cleaned_data.get('has_disabled_access')

            # Filter tables based on preferences
            tables = Table.objects.all()  # Start with all tables

            if is_quiet == 1:  # True
                tables = tables.filter(is_quiet=True)
            elif is_quiet == 2:  # False
                tables = tables.filter(is_quiet=False)

            if is_outside == 1:  # True
                tables = tables.filter(is_outside=True)
            elif is_outside == 2:  # False
                tables = tables.filter(is_outside=False)

            if has_bench_seating == 1:  # True
                tables = tables.filter(has_bench_seating=True)
            elif has_bench_seating == 2:  # False
                tables = tables.filter(has_bench_seating=False)

            if has_disabled_access == 1:  # True
                tables = tables.filter(has_disabled_access=True)
            elif has_disabled_access == 2:  # False
                tables = tables.filter(has_disabled_access=False)

            # Apply odd/even logic based on reservation date
            if half_full:
                available_tables = tables
            else:
                # Apply odd/even logic based on the reservation date
                if reservation_date.day % 2 == 0:
                    available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 == 0])
                else:
                    available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 != 0])

            # # Check for overlapping reservations
            # available_tables = available_tables.filter(
            #     ~Q(reservation__reservation_date__lt=reservation_date + timedelta(hours=2)) &
            #     ~Q(reservation__reservation_date__gt=reservation_date)
            # ).distinct()

            # # Calculate the reservation end dynamically instead of querying the database
            # reserved_table_ids = Reservation.objects.filter(
            #     Q(reservation_date__lt=reservation_date + timedelta(hours=2)) &  # Calculate the dynamic end time
            #     Q(reservation_date__gt=reservation_date - timedelta(hours=2))  # Adjust this for overlap checking
            # ).values_list('tables', flat=True)

            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                Q(reservation_date__lt=reservation_end) &
                Q(reservation_date__gt=reservation_date - timedelta(hours=2))
            )
            reserved_table_ids = overlapping_reservations.values_list('tables', flat=True)

            available_tables = available_tables.exclude(pk__in=reserved_table_ids)

            # Debugging: Show available tables
            table_details = ', '.join([str(table) for table in available_tables])
            form.add_error(None, f'Available tables: {table_details}')  

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