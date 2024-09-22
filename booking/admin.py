from django.contrib import admin
from .models import Reservation, Table, OpeningTime, ReservationTimeSpan
from django_summernote.admin import SummernoteModelAdmin
from .models import SiteSettings
from django.utils.translation import gettext_lazy as _


"""
Admin Configuration - Sites
"""
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site', 'contact_email', 'phone_number']


"""
Admin Configuration for Opening Times
"""
@admin.register(OpeningTime)
class OpeningTimeAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'open_time', 'close_time')
    list_filter = ('day_of_week',)
    search_fields = ('day_of_week',)


"""
 Admin Configuration for Reservation Time Spans
"""
@admin.register(ReservationTimeSpan)
class ReservationTimeSpanAdmin(admin.ModelAdmin):
    list_display = ('party_size', 'duration')
    list_filter = ('party_size',)
    search_fields = ('party_size',)

"""
Admin Configuration - Tables
"""
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'formatted_zone', 'capacity', 'vip_category', 'is_quiet', 'is_outside', 'note')
    search_fields = ('table_number', 'zone')
    list_filter = ('vip_category', 'is_quiet', 'is_outside', 'has_bench_seating', 'has_disabled_access')

    def formatted_zone(self, obj):
        return f"Zone {obj.zone}"
    formatted_zone.short_description = 'Zone'  # This is the display name in the admin panel


"""
HourFilter Class for Reservations
"""
class HourFilter(admin.SimpleListFilter):
    title = _('Reservation Hour')
    parameter_name = 'reservation_hour'

    def lookups(self, request, model_admin):
        # Provide a dropdown list of hours (0-23)
        return [(str(i), f"{i:02}:00") for i in range(24)]  # Dropdown options in HH:00 format

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reservation_date__hour=self.value())
        return queryset


"""
TableNumberFilter Class for Reservations
"""
class TableNumberFilter(admin.SimpleListFilter):
    title = _('Table Number')
    parameter_name = 'table_number'

    def lookups(self, request, model_admin):
        # Fetch all tables ordered by table number
        tables = Table.objects.all().order_by('table_number')
        return [(table.pk, f"Table {table.table_number}") for table in tables]  # Dropdown with sorted table numbers

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tables__pk=self.value())


"""
ZoneNumberFilter Class for Reservations
"""
class ZoneFilter(admin.SimpleListFilter):
    title = _('Zone')
    parameter_name = 'zone'

    def lookups(self, request, model_admin):
        # Get all available zones from the tables
        zones = Table.objects.values_list('zone', flat=True).distinct().order_by('zone')
        return [(zone, f"Zone {zone}") for zone in zones]  # Dropdown with unique zones

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tables__zone=self.value())
        return queryset


"""
Admin Configuration for Reservations
"""
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation_date', 'guest_count', 'status', 'assigned_tables', 'created_on')
    search_fields = ['user__username', 'reservation_date', 'guest_count', 'status']
    
    # Order of filters in the admin panel, with dropdowns for Hour, Table Number, and Zone
    list_filter = ('status', 'reservation_date', 'created_on', HourFilter, TableNumberFilter, ZoneFilter)
    
    date_hierarchy = 'reservation_date'
    readonly_fields = ('created_on', 'updated_on', 'created_by', 'edited_by')

    def assigned_tables(self, obj):
        return ", ".join(f"Table {table.table_number} (Z{table.zone})" for table in obj.tables.all())
    assigned_tables.short_description = 'Assigned Tables'

