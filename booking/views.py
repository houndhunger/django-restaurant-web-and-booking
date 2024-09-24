from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.db.models import Case, When, Value
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    View, TemplateView, DetailView, UpdateView, DeleteView, CreateView)
from datetime import datetime, timedelta
from django.contrib import messages
from .models import Reservation, OpeningTime
from .models import Reservation, Table, ReservationTimeSpan
from .forms import ReservationForm, CustomSignupForm
from .utils.reservation_utils import (
    check_email_unique, handle_reservation_logic)
from allauth.account.views import SignupView


class UserReservationsView(generic.ListView):
    """
    View to list the reservations for the currently logged-in user
    """
    model = Reservation
    template_name = 'booking/user_reservations.html'
    paginate_by = 3

    def get_queryset(self):
        now = timezone.now()
        # Filter for future reservations, exclude those with
        # status 2 or 3, and order by reservation date and time
        return Reservation.objects.filter(
            user=self.request.user,
            reservation_date__gt=now
        ).exclude(status__in=[2, 3]).order_by('reservation_date')


DAYS_ORDER = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6,
}


class BaseReservationView(LoginRequiredMixin):
    """
    Base View for Make and Edit reservation
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'booking/reservation_make_edit.html'

    def handle_form(self, form, original_reservation=None):
        try:
            # Get reservation date and guest count from the form
            reservation_date = form.cleaned_data.get('reservation_date')
            guest_count = form.cleaned_data.get('guest_count')

            # Calculate reservation_end_date based on guest_count
            reservation_time_span = ReservationTimeSpan.objects.get(
                guest_count=guest_count
            )
            reservation_end_date = (
                reservation_date + reservation_time_span.duration
            )

            # Create reservation instance
            reservation = form.save(commit=False)
            reservation.reservation_end_date = reservation_end_date
            reservation.user = self.request.user
            reservation.status = 1  # Set status to 'Confirmed'

            # Call the existing handle_reservation_logic function
            reservation, available_tables = handle_reservation_logic(
                form, self.request.user, original_reservation)

            # If reservation is None, form has an error
            if reservation is None:
                return self.form_invalid(form)

            # Save the reservation and assigned tables
            reservation.save()
            reservation.tables.set(available_tables[:reservation.guest_count])
            return redirect(
                reverse('preview_reservation', kwargs={'pk': reservation.pk})
            )

        except ReservationTimeSpan.DoesNotExist:
            form.add_error(None, "Invalid guest count for reservation.")
            return self.form_invalid(form)
        except forms.ValidationError as e:
            # Add the error message to the form
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        form.data = form.data.copy()

        if 'reservation_date' in form.data:
            # Format the date to match 'Y/m/d H:i'
            try:
                date_str = form.data['reservation_date']
                formatted_date = datetime.strptime(
                    date_str, '%d %b %Y, %H:%M').strftime('%Y/%m/%d %H:%M')
                form.data['reservation_date'] = formatted_date
            except ValueError:
                pass  # In case the date format is not what we expect

        return self.render_to_response(self.get_context_data(form=form))

    # Display corresponding header and Opening Times
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use a header value from child classes
        context['header'] = self.header
        # Retrieve OpeningTime objects sorted by actual day of the week
        context['opening_times'] = self.get_opening_times()
        # Control visibility
        context['show_opening_time_table'] = context['opening_times']
        return context

    def get_opening_times(self):
        # Custom sorting by day_of_week using Django's Case-When
        ordering_case = Case(
            When(day_of_week='mon', then=Value(0)),
            When(day_of_week='tue', then=Value(1)),
            When(day_of_week='wed', then=Value(2)),
            When(day_of_week='thu', then=Value(3)),
            When(day_of_week='fri', then=Value(4)),
            When(day_of_week='sat', then=Value(5)),
            When(day_of_week='sun', then=Value(6)),
        )

        # Return the queryset ordered by the mapped values for day_of_week
        return OpeningTime.objects.annotate(
            day_sort_order=ordering_case
        ).order_by('day_sort_order')


class MakeReservationView(BaseReservationView, CreateView):
    """
    View to make a new reservation
    """
    header = 'Make a Reservation'

    def form_valid(self, form):
        return self.handle_form(form)


class EditReservationView(BaseReservationView, UpdateView):
    """
    View to edit an existing reservation
    """
    header = 'Edit Reservation'

    def form_valid(self, form):
        # Retrieve the original reservation
        original_reservation = self.get_object()
        # Pass it to handle_form - custom method
        return self.handle_form(form, original_reservation)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass reservation instance to the form
        kwargs['instance'] = self.get_object()
        return kwargs


class ReservationPreviewView(LoginRequiredMixin, DetailView):
    """
    View to preview reservation
    """
    model = Reservation
    template_name = 'booking/reservation_preview.html'
    context_object_name = 'reservation'

    def get_object(self, queryset=None):
        # Get the reservation ID from the query parameters
        reservation_id = self.kwargs.get('pk')
        # Retrieve the reservation object
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        return reservation


class DeleteReservationView(LoginRequiredMixin, View):
    """
    View to delete a reservation
    """
    template_name = 'booking/reservation_delete.html'
    success_url = reverse_lazy('user_reservations')

    def get(self, request, *args, **kwargs):
        reservation = self.get_object()
        return render(
            request, self.template_name, {'reservation': reservation})

    def post(self, request, *args, **kwargs):
        reservation = self.get_object()
        # Change the status to 3 (indicating it's "deleted"
        # but not actually removed)
        reservation.status = 3
        reservation.save()
        return redirect(self.success_url)

    def get_object(self):
        return get_object_or_404(
            Reservation, id=self.kwargs['pk'], user=self.request.user)


class CustomSignupView(SignupView):
    """
    View to Signup
    """
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
        return reverse_lazy('home')  # Adjust 'home' to the appropriate URL

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
