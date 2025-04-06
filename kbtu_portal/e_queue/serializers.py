from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='get_course')  # Используем метод get_course
    specialty = serializers.CharField(source='get_specialty')  # Используем метод get_specialty

    class Meta:
        model = Appointment
        fields = ['id', 'student', 'name', 'course', 'specialty', 'date', 'time', 'status', 'rejection_reason', 'manager']
