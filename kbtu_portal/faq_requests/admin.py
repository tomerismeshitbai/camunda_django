from django.contrib import admin
from .models import FAQRequest

@admin.register(FAQRequest)
class FAQRequestAdmin(admin.ModelAdmin):
    pass
