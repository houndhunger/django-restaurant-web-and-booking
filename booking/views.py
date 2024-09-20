from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, CreateView
from datetime import datetime, timedelta
from django.contrib import messages

# Models and forms
from .models import Reservation, Table
from .forms import ReservationForm, CustomSignupForm

# Utilities
from .utils.reservation_utils import check_email_unique, handle_reservation_logic

# Allauth
from allauth.account.views import SignupView


"""
View to list all reservations (staff, not guest)
"""
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


"""
View to list all tables (staff, not guest)
"""
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


"""
View to list the reservations for the currently logged-in user
"""
class UserReservationsView(generic.ListView):
    model = Reservation
    template_name = 'booking/user_reservations.html'
    paginate_by = 6

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

"""
View to make a new reservation
"""
class MakeReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_make_edit.html'

    def form_valid(self, form):
        reservation, available_tables = handle_reservation_logic(form, self.request.user)
        if available_tables.exists():
            reservation.save()
            reservation.tables.set(available_tables[:reservation.guest_count])
            return redirect(reverse('preview_reservation', kwargs={'pk': reservation.pk}))
        else:
            form.add_error(None, 'No available tables for the selected date and preferences.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Retain the submitted date value for Flatpickr
        form.data = form.data.copy()  # Copy the form data to modify it
        if 'reservation_date' in form.data:
            # Format the date to match 'Y/m/d H:i'
            try:
                date_str = form.data['reservation_date']
                # Ensure it's in the correct format (adjust as needed)
                formatted_date = datetime.strptime(date_str, '%d %b %Y, %H:%M').strftime('%Y/%m/%d %H:%M')
                form.data['reservation_date'] = formatted_date
            except ValueError:
                pass  # In case the date format is not what we expect

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Make a Reservation'
        return context


"""
View to preview reservation
"""
class ReservationPreviewView(DetailView):
    model = Reservation
    template_name = 'booking/reservation_preview.html'
    context_object_name = 'reservation'

    def get_object(self, queryset=None):
        # Get the reservation ID from the query parameters
        reservation_id = self.kwargs.get('pk')
        # Retrieve the reservation object
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        return reservation


"""
View edit existing reservation
"""
class EditReservationView(LoginRequiredMixin, UpdateView):
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
            return redirect(reverse('preview_reservation', kwargs={'pk': reservation.pk}))
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

"""
View to delete a reservation
"""
class DeleteReservationView(DeleteView):
    model = Reservation
    template_name = 'booking/reservation_delete.html'
    success_url = reverse_lazy('user_reservations')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, id=self.kwargs['pk'], user=self.request.user)

"""
View to Signup
"""
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