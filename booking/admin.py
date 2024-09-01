from django.contrib import admin
from .models import Reservation
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation_date', 'guest_count', 'status', 'created_on', 'updated_on')
    search_fields = ['user__username', 'reservation_date', 'guest_count', 'status']
    list_filter = ('status', 'reservation_date', 'created_on')
    date_hierarchy = 'reservation_date'
    readonly_fields = ('created_on', 'updated_on', 'created_by', 'edited_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is new (being created)
            obj.created_by = request.user
        obj.edited_by = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
# admin.site.register(Reservation)