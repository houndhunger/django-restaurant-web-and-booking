"""
Django Admin Configuration for the booking app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reservation, Table, OpeningTime, ReservationTimeSpan, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin Configuration - Sites
    """
    verbose_name = "Site Setting"  # Singular name
    verbose_name_plural = "Site Setting"  # Plural name
    list_display = ['site', 'contact_email', 'phone_number']


@admin.register(OpeningTime)
class OpeningTimeAdmin(admin.ModelAdmin):
    """
    Admin Configuration for Opening Times
    """
    list_display = ('day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week',)
    search_fields = ('day_of_week',)


@admin.register(ReservationTimeSpan)
class ReservationTimeSpanAdmin(admin.ModelAdmin):
    """
    Admin Configuration for Reservation Time Spans
    """
    list_display = ('guest_count', 'duration')
    list_filter = ('guest_count',)
    search_fields = ('guest_count',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    Admin Configuration - Tables
    """
    list_display = (
        'table_number', 'formatted_zone', 'capacity',
        'vip_category', 'is_quiet', 'is_outside', 'note'
    )
    search_fields = ('table_number', 'zone')
    list_filter = (
        'vip_category', 'is_quiet', 'is_outside',
        'has_bench_seating', 'has_disabled_access'
    )

    def formatted_zone(self, obj):
        """
        Display the formatted zone in the admin panel.
        """
        return f"Zone {obj.zone}"

    formatted_zone.short_description = 'Zone'


class HourFilter(admin.SimpleListFilter):
    """
    HourFilter Class for Reservations
    """
    title = _('Reservation Hour')
    parameter_name = 'reservation_hour'

    def lookups(self, request, model_admin):
        """
        Provide a dropdown list in HH:00 format.
        """
        return [(str(i), f"{i:02}:00") for i in range(24)]

    def queryset(self, request, queryset):
        """
        Return filtered queryset based on selected hour.
        """
        if self.value():
            return queryset.filter(reservation_date__hour=self.value())
        return queryset


class TableNumberFilter(admin.SimpleListFilter):
    """
    TableNumberFilter Class for Reservations
    """
    title = _('Table Number')
    parameter_name = 'table_number'

    def lookups(self, request, model_admin):
        """
        Fetch all tables ordered by table number.
        """
        tables = Table.objects.all().order_by('table_number')
        return [(table.pk, f"Table {table.table_number}") for table in tables]

    def queryset(self, request, queryset):
        """
        Return filtered queryset based on selected table number.
        """
        if self.value():
            return queryset.filter(tables__pk=self.value())
        return queryset


class ZoneFilter(admin.SimpleListFilter):
    """
    ZoneNumberFilter Class for Reservations
    """
    title = _('Zone')
    parameter_name = 'zone'

    def lookups(self, request, model_admin):
        """
        Get all available zones from the tables.
        """
        zones = Table.objects.values_list('zone', flat=True).distinct().order_by('zone')
        return [(zone, f"Zone {zone}") for zone in zones]

    def queryset(self, request, queryset):
        """
        Return filtered queryset based on selected zone.
        """
        if self.value():
            return queryset.filter(tables__zone=self.value())
        return queryset


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin Configuration for Reservations
    """
    list_display = (
        'user', 'reservation_date', 'reservation_end_date',
        'guest_count', 'status', 'assigned_tables', 'created_on'
    )
    search_fields = [
        'user__username', 'reservation_date',
        'guest_count', 'status'
    ]
    list_filter = (
        'status', 'reservation_date', 'created_on',
        HourFilter, TableNumberFilter, ZoneFilter
    )
    date_hierarchy = 'reservation_date'
    readonly_fields = ('created_on', 'updated_on', 'created_by', 'edited_by')

    def assigned_tables(self, obj):
        """
        Return a list of assigned tables.
        """
        tables_list = [
            f"Table {table.table_number} (Z{table.zone})"
            for table in obj.tables.all()
        ]
        return ", ".join(tables_list)

    assigned_tables.short_description = 'Assigned Tables'
