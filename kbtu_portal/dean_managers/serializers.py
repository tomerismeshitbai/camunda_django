from rest_framework import serializers
from .models import ManagerProfile

class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ['user', 'first_name', 'last_name', 'middle_name', 'email', 'school', 'phone_number', 'role', 'position']
