from django.contrib import admin
from .models import Reservation, Table
from django_summernote.admin import SummernoteModelAdmin
from .models import SiteSettings
from django.utils.translation import gettext_lazy as _


"""
admin - Sites
"""
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site', 'contact_email', 'phone_number']


"""
admin - Tables
"""
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'zone', 'capacity', 'vip_category', 'is_quiet', 'is_outside', 'note')
    search_fields = ('table_number', 'zone')
    list_filter = ('vip_category', 'is_quiet', 'is_outside')

"""
HourFilter class
"""
class HourFilter(admin.SimpleListFilter):
    title = _('Reservation Hour')
    parameter_name = 'reservation_hour'

    def lookups(self, request, model_admin):
        return [(str(i), str(i)) for i in range(24)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reservation_date__hour=self.value())
        return queryset

"""
admin - Reservations
"""
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation_date', 'guest_count', 'status', 'assigned_tables', 'created_on')
    search_fields = ['user__username', 'reservation_date', 'guest_count', 'status']
    list_filter = ('status', 'reservation_date', 'created_on', HourFilter)
    date_hierarchy = 'reservation_date'
    readonly_fields = ('created_on', 'updated_on', 'created_by', 'edited_by')

    def assigned_tables(self, obj):
        return ", ".join(f"Table {table.table_number} (Z{table.zone})" for table in obj.tables.all())
    assigned_tables.short_description = 'Assigned Tables'  # Column title in the admin view

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is new (being created)
            obj.created_by = request.user
        obj.edited_by = request.user
        super().save_model(request, obj, form, change)


