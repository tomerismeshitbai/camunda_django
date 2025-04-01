from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQRequestAdmin(admin.ModelAdmin):
    pass
