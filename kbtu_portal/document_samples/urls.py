from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DownloadInvitationPDF,
    InvitationLetterCreateView,
    InvitationLetterListView,
    InvitationLetterDetailView,
    DownloadPreDiplomaInvitationPDF,
    DocumentSampleViewSet
)

router = DefaultRouter()
router.register(r'documents', DocumentSampleViewSet)


urlpatterns = [
    path('invitation/<int:pk>/pdf/', DownloadInvitationPDF.as_view(), name='invitation-pdf'),  
    path('invitation_prediploma/<int:pk>/pdf/', DownloadPreDiplomaInvitationPDF.as_view(), name='invitation-pdf'), 
    path('invitation/create/', InvitationLetterCreateView.as_view(), name='invitation-create'), 
    path('invitations/', InvitationLetterListView.as_view(), name='invitation-list'),  
    path('invitation/<int:pk>/', InvitationLetterDetailView.as_view(), name='invitation-detail'),


    path('', include(router.urls)), 
]
