from django.contrib import admin
from .models import Task, Attachment

admin.site.register(Task)
admin.site.register(Attachment)