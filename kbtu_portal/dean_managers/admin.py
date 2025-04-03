from django.contrib import admin
from .models import ManagerProfile

class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'email', 'phone_number', 'role', 'school')
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['role', 'school']

admin.site.register(ManagerProfile, ManagerProfileAdmin)
