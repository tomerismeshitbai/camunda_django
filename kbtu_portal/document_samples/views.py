from rest_framework import serializers, generics
from document_samples.models import InvitationLetter
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from document_samples.utils.generate_invitation_pdf import generate_invitation_pdf
from document_samples.utils.generate_invitation_2_pdf import generate_invitation_2_pdf
from .serializers import InvitationLetterSerializer



class DownloadInvitationPDF(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        invitation = get_object_or_404(InvitationLetter, pk=pk)
        return generate_invitation_pdf(invitation.id)

class DownloadPreDiplomaInvitationPDF(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        invitation = get_object_or_404(InvitationLetter, pk=pk)
        return generate_invitation_2_pdf(invitation.id)



class InvitationLetterCreateView(generics.CreateAPIView):
    queryset = InvitationLetter.objects.all()
    serializer_class = InvitationLetterSerializer

class InvitationLetterListView(generics.ListAPIView):
    queryset = InvitationLetter.objects.all()
    serializer_class = InvitationLetterSerializer
    
class InvitationLetterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvitationLetter.objects.all()
    serializer_class = InvitationLetterSerializer
