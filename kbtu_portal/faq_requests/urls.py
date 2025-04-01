from django.urls import path
from .views import FAQRequestCreateView, FAQRequestListView, FAQRequestDetailView

urlpatterns = [
    path('', FAQRequestListView.as_view(), name='faq-request-list'),
    path('create/', FAQRequestCreateView.as_view(), name='faq-request-create'),
    path('<int:pk>/', FAQRequestDetailView.as_view(), name='faq-request-detail'),
]
