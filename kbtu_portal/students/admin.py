from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "kbtu_id", "email", "course", "role")
    search_fields = ("first_name", "last_name", "kbtu_id", "email")
    list_filter = ("school", "speciality", "course", "role")