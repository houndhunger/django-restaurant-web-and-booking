from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, CreateView
from datetime import datetime, timedelta
from django.contrib import messages
from .models import Reservation 

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
Base View for Make and Edit reservation
"""
class BaseReservationView(LoginRequiredMixin):
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_make_edit.html'

    def handle_form(self, form, original_reservation=None):
        # # Check for existing errors in the form
        # if not form.is_valid():
        #     return self.form_invalid(form)

        try:
            reservation, available_tables = handle_reservation_logic(form, self.request.user, original_reservation)
            
            # If reservation is None, form has an error (e.g., overlapping reservation)
            if reservation is None:
                return self.form_invalid(form)  # Return the form with the error displayed
            
            # Save the reservation and assigned tables
            reservation.save()
            reservation.tables.set(available_tables[:reservation.guest_count])
            return redirect(reverse('preview_reservation', kwargs={'pk': reservation.pk}))

        except forms.ValidationError as e:
            form.add_error(None, str(e))  # Add the error message to the form
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Retain the submitted date value for Flatpickr
        form.data = form.data.copy()  # Copy the form data to modify it

        if 'reservation_date' in form.data:
            # Format the date to match 'Y/m/d H:i'
            try:
                date_str = form.data['reservation_date']
                formatted_date = datetime.strptime(date_str, '%d %b %Y, %H:%M').strftime('%Y/%m/%d %H:%M')
                form.data['reservation_date'] = formatted_date
            except ValueError:
                pass  # In case the date format is not what we expect

        return self.render_to_response(self.get_context_data(form=form))

    # to display coresponding header
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = self.header  # Use a header value from child classes
        return context



"""
View to make a new reservation
"""
class MakeReservationView(BaseReservationView, CreateView):
    header = 'Make a Reservation'

    def form_valid(self, form):
        print("MakeReservationView: form_valid RUNS")
        return self.handle_form(form)


"""
View to edit an existing reservation
"""
class EditReservationView(BaseReservationView, UpdateView):
    header = 'Edit Reservation'

    def form_valid(self, form):
        original_reservation = self.get_object()  # Retrieve the original reservation
        return self.handle_form(form, original_reservation)  # Pass it to handle_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()  # Pass reservation instance to the form
        return kwargs


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