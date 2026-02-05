from django.shortcuts import render

from rest_framework import generics, permissions

from .models import Status
from .serializers import StatusSerializer
# Create your views here.


class StatusListGetView(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatusRudView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAdminUser]


class StatusCreateView(generics.CreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAdminUser]
