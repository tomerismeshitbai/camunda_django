from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework.filters import SearchFilter

class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.filter(published=True)
    serializer_class = FAQSerializer
    filter_backends = [SearchFilter]
    search_fields = ['question', 'answer']
