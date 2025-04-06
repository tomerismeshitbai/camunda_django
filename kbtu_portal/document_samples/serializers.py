from rest_framework import serializers, generics
from .models import InvitationLetter, CourseRegistrationApplication, DocumentSample

class DocumentSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSample
        fields = '__all__'



class CourseRegistrationApplicationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='student.first_name', read_only=True)
    last_name = serializers.CharField(source='student.last_name', read_only=True)
    middle_name = serializers.CharField(source='student.middle_name', read_only=True)
    kbtu_id = serializers.CharField(source='student.kbtu_id', read_only=True)
    course = serializers.IntegerField(source='student.course', read_only=True)
    speciality = serializers.CharField(source='student.speciality', read_only=True)
    telephone_number = serializers.CharField(source='student.telephone_number', read_only=True)
    email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = CourseRegistrationApplication
        fields = '__all__'


class InvitationLetterSerializer(serializers.ModelSerializer):
    course = serializers.IntegerField(required=False)
    speciality = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)

    class Meta:
        model = InvitationLetter
        fields = [
            'id', 'student',
            'first_name', 'last_name', 'middle_name',
            'course', 'speciality',
            'organization_name', 'start_date', 'end_date',
            'supervisor_name', 'supervisor_position',
            'current_year'
        ]
        read_only_fields = ['current_year']

    def create(self, validated_data):
        student = validated_data.get("student", None)

        if student:
            # Подтягиваем данные из StudentProfile
            validated_data['first_name'] = student.first_name
            validated_data['last_name'] = student.last_name
            validated_data['middle_name'] = student.middle_name
            validated_data['course'] = student.course
            validated_data['speciality'] = student.speciality

        return super().create(validated_data)

