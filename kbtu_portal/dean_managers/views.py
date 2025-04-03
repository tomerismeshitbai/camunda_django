from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import ManagerProfile
from .serializers import ManagerProfileSerializer

class ManagerProfileViewSet(viewsets.ModelViewSet):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']  
