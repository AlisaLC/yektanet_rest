from rest_framework import generics, permissions

from employer.models import Employer
from employer.permissions import IsOwnerOrReadOnly
from employer.serializers import EmployerRegisterSerializer, EmployerSerializer


class EmployerRegisterView(generics.CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerRegisterSerializer


class EmployerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
