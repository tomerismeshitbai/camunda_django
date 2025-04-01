from rest_framework import serializers
from .models import FAQRequest

class FAQRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQRequest
        fields = '__all__'
