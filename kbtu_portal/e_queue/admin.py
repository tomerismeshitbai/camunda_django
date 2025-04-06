from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'date', 'time', 'status', 'manager')
    list_filter = ('status', 'date', 'manager')
    search_fields = ('name', 'student__first_name', 'student__last_name')

admin.site.register(Appointment, AppointmentAdmin)
