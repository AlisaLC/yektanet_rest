from rest_framework import generics, permissions

from applicant.models import Applicant
from applicant.permissions import IsOwnerOrReadOnly
from applicant.serializers import ApplicantRegisterSerializer, ApplicantSerializer


class ApplicantRegisterView(generics.CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantRegisterSerializer


class ApplicantRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
