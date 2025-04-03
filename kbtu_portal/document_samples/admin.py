from django.contrib import admin
from .models import Course, CourseRegistrationApplication, InvitationLetter


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits_kz', 'credits_ects', 'retake')
    search_fields = ('code', 'name')
    list_filter = ('retake',)


@admin.register(CourseRegistrationApplication)
class CourseRegistrationApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'created_at')
    search_fields = ('student__user__username', 'student__kbtu_id')
    list_filter = ('semester', 'created_at')
    filter_horizontal = ('courses',)


@admin.register(InvitationLetter)
class InvitationLetterAdmin(admin.ModelAdmin):
    list_display = ('student', 'organization_name', 'start_date', 'end_date', 'supervisor_name', 'created_at')
    search_fields = ('student__user__username', 'organization_name', 'supervisor_name')
    list_filter = ('start_date', 'end_date', 'created_at')


