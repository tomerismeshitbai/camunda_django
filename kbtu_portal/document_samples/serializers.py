from rest_framework import serializers, generics
from .models import InvitationLetter, CourseRegistrationApplication

class CourseRegistrationApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    kbtu_id = serializers.CharField(source='student.kbtu_id', read_only=True)
    course = serializers.IntegerField(source='student.course', read_only=True)
    speciality = serializers.CharField(source='student.speciality', read_only=True)
    telephone_number = serializers.CharField(source='student.telephone_number', read_only=True)
    email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = CourseRegistrationApplication
        fields = '__all__'


class InvitationLetterSerializer(serializers.ModelSerializer):
    course = serializers.IntegerField(source='student.course', read_only=True)
    speciality = serializers.CharField(source='student.speciality', read_only=True)
    first_name = serializers.CharField(source='student.first_name', read_only=True)
    last_name = serializers.CharField(source='student.last_name', read_only=True)
    middle_name = serializers.CharField(source='student.middle_name', read_only=True)  # Если middle_name в модели StudentProfile
    current_year = serializers.IntegerField(read_only=True)

    class Meta:
        model = InvitationLetter
        fields = [
            'id', 'student', 'organization_name', 'course', 'speciality', 
            'first_name', 'last_name', 'middle_name',  
            'start_date', 'end_date', 'supervisor_name', 'supervisor_position', 'current_year'
        ]
        read_only_fields = ['course', 'speciality', 'first_name', 'last_name', 'middle_name', 'current_year']
