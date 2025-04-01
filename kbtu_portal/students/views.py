from rest_framework import generics
from students.models import StudentProfile
from students.serializers import StudentProfileSerializer

class StudentProfileDetailView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field = 'id' 

class StudentProfileUpdateView(generics.UpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field = 'id'