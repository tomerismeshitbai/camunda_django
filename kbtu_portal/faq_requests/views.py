from rest_framework import generics, permissions
from .models import FAQRequest
from .serializers import FAQRequestSerializer

class FAQRequestCreateView(generics.CreateAPIView):
    queryset = FAQRequest.objects.all()
    serializer_class = FAQRequestSerializer
    # permission_classes = [permissions.IsAuthenticated]

class FAQRequestListView(generics.ListAPIView):
    queryset = FAQRequest.objects.all()
    serializer_class = FAQRequestSerializer
    # permission_classes = [permissions.IsAdminUser]

class FAQRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = FAQRequest.objects.all()
    serializer_class = FAQRequestSerializer
    # permission_classes = [permissions.IsAdminUser]
