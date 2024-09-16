from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from allauth.account.forms import SignupForm
from django.db.models import Q
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Reservation, Table
from .forms import ReservationForm, CustomSignupForm
from datetime import timedelta

# Check email unique
from .utils.reservation_utils import check_email_unique

# for Custom Signup View
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.models import User


# Home view...
class HomeView(TemplateView):
    template_name = 'index.html'

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


#from .utils import handle_reservation_logic  # Import from utils
#from myapp.utils.reservation_utils import handle_reservation_logic
from .utils.reservation_utils import handle_reservation_logic  # Import the function

class MakeReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_make_edit.html'

    def form_valid(self, form):
        reservation, available_tables = handle_reservation_logic(form, self.request.user)
        if available_tables.exists():
            reservation.save()
            reservation.tables.set(available_tables[:reservation.guest_count])
            return redirect(reverse('user_reservations'))
        else:
            form.add_error(None, 'No available tables for the selected date and preferences.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Make a Reservation'
        return context

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_make_edit.html'

    # Overrides the method to pass the reservation instance to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Ensure that the form is initialized with the reservation instance
        kwargs['instance'] = self.get_object()
        return kwargs

    # Handles form submission and reservation logic
    def form_valid(self, form):
        print("Form cleaned data:", form.cleaned_data)
        # Process reservation and available tables based on user input
        reservation, available_tables = handle_reservation_logic(form, self.request.user)
        print("Form is valid. Reservation data:", reservation)
        print("Available tables:", available_tables)

        # If tables are available, save the reservation and assign tables
        if available_tables.exists():
            reservation.save()
            reservation.tables.set(available_tables[:reservation.guest_count])
            print("Reservation saved with tables:", reservation.tables.all())
            return redirect(reverse('user_reservations'))
        else:
            # If no tables are available, show an error on the form
            form.add_error(None, 'No available tables for the selected date and preferences.')
            return self.form_invalid(form)

    # Adds custom data to the context for rendering the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Edit Reservation'
        print("Context data:", context)
        return context

    # Retrieves the reservation object that is being edited
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print("Loaded reservation object:", obj)
        return obj

    # Handles form submission errors and logs them
    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)


# # View to make a new reservation
# class MakeReservationView(LoginRequiredMixin, CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'booking/reservation_make_edit.html'

#     def form_valid(self, form):
#         form.instance.user = self.request.user  # Associate the logged-in user
#         # Other reservation logic here...

#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['header'] = 'Make a Reservation'
#         return context

#     # def test_func(self):
#     #     # Custom check: ensure the user is staff
#     #     return self.request.user.is_staff

#     # def handle_no_permission(self):
#     #     if not self.request.user.is_authenticated:
#     #         # Redirect to login page if not authenticated
#     #         return redirect('login')  # Adjust 'login' to your login URL name
#     #     # Handle other permission failures
#     #     return super().handle_no_permission()

#     def get(self, request, *args, **kwargs):
#         form = ReservationForm()
#         return render(request, self.template_name, {'form': form, 'header': 'Make a Reservation'})

#     def post(self, request, *args, **kwargs):
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user  # Associate the logged-in user

#             # Get reservation details
#             reservation_date = reservation.reservation_date
#             reservation_end = reservation_date + timedelta(hours=2)  # Default 2-hour duration

#             # Calculate total tables and reserved tables
#             total_tables = Table.objects.count()
#             reserved_tables_count = Reservation.objects.filter(
#                 reservation_date__date=reservation_date.date(),
#                 status=1
#             ).count()

#             # # Debugging: Log the total and reserved tables count
#             # print(f'Total tables: {total_tables}, Reserved tables: {reserved_tables_count}')

#             # Determine if the restaurant is more than half full
#             half_full = reserved_tables_count >= total_tables / 2

#             # Extract preferences from the form
#             is_quiet = form.cleaned_data.get('is_quiet')
#             is_outside = form.cleaned_data.get('is_outside')
#             has_bench_seating = form.cleaned_data.get('has_bench_seating')
#             has_disabled_access = form.cleaned_data.get('has_disabled_access')

#             # Filter tables based on preferences
#             tables = Table.objects.all()  # Start with all tables
#             # Apply preferences only if set, otherwise bypass
#             for key, value in preferences.items():
#                 if value == 'yes':
#                     tables = tables.filter(**{key: True})
#                 elif value == 'no':
#                     tables = tables.filter(**{key: False})

#             # Apply odd/even logic based on reservation date
#             if half_full:
#                 available_tables = tables
#             else:
#                 # Apply odd/even logic based on the reservation date
#                 if reservation_date.day % 2 == 0:
#                     available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 == 0])
#                 else:
#                     available_tables = tables.filter(pk__in=[t.pk for t in Table.objects.all() if t.pk % 2 != 0])

#             # # Check for overlapping reservations
#             # available_tables = available_tables.filter(
#             #     ~Q(reservation__reservation_date__lt=reservation_date + timedelta(hours=2)) &
#             #     ~Q(reservation__reservation_date__gt=reservation_date)
#             # ).distinct()

#             # # Calculate the reservation end dynamically instead of querying the database
#             # reserved_table_ids = Reservation.objects.filter(
#             #     Q(reservation_date__lt=reservation_date + timedelta(hours=2)) &  # Calculate the dynamic end time
#             #     Q(reservation_date__gt=reservation_date - timedelta(hours=2))  # Adjust this for overlap checking
#             # ).values_list('tables', flat=True)

#             # Check for overlapping reservations
#             overlapping_reservations = Reservation.objects.filter(
#                 Q(reservation_date__lt=reservation_end) &
#                 Q(reservation_date__gt=reservation_date - timedelta(hours=2))
#             )
#             reserved_table_ids = overlapping_reservations.values_list('tables', flat=True)

#             available_tables = available_tables.exclude(pk__in=reserved_table_ids)

#             # # Debugging: Show available tables
#             # table_details = ', '.join([str(table) for table in available_tables])
#             # form.add_error(None, f'Available tables: {table_details}')  

#             # # Debugging: Show available tables
#             # print(f'Available tables: {available_tables}')

#             # Assign tables if available
#             if available_tables.exists():
#                 reservation.save()
#                 reservation.tables.set(available_tables[:reservation.guest_count])  # Assign tables based on guest count
#                 return redirect(reverse('user_reservations'))
#             else:
#                 # Return form with error if no tables are available
#                 form.add_error(None, 'No available tables for the selected date and preferences.')
#         # else:
#         #     # Debugging: Show form errors
#         #     print(f'Form errors: {form.errors}')

#         return render(request, self.template_name, {'form': form, 'header': 'Make a Reservation'})

# # View to edit reservation
# class EditReservationView(UpdateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'booking/reservation_edit.html'
#     success_url = reverse_lazy('user_reservations')  # Redirect after successful update

#     def get_object(self, queryset=None):
#         # Ensure that the object being edited is the one in the URL
#         return super().get_object(queryset)


# View to delete a reservation
class DeleteReservationView(DeleteView):
    model = Reservation
    template_name = 'booking/reservation_delete.html'
    success_url = reverse_lazy('user_reservations')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, id=self.kwargs['pk'], user=self.request.user)

# View to Signup
class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            # If email is not unique, add an error message
            form.add_error('email', 'The email address is already in use.')
            return self.form_invalid(form)
        
        # If email is unique, proceed with form processing
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a success page or home page after successful signup
        return reverse_lazy('home')  # Adjust 'home' to the appropriate URL name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_feedback'] = self.request.GET.get('email_feedback', '')
        return context
    
    def non_field_errors(self):
        # Customize non-field errors to remove `__all__:` prefix.
        errors = super().non_field_errors()
        if errors:
            return errors.replace('__all__: ', '')
        return errors


# # View to user login
# class LogInView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/login.html'


# from allauth.account.views import LoginView

# class CustomLoginView(LoginView):
#     form_class = CustomLoginForm
#     template_name = 'login.html'


# def signup_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to a success page
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'account/signup.html', {'form': form})
