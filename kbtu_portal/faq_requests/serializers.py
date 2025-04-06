from rest_framework import serializers
from .models import FAQRequest
from students.models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['first_name', 'last_name', 'kbtu_id','course','speciality']

class FAQRequestSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = FAQRequest
        fields = '__all__'
