from django.shortcuts import render

from rest_framework import generics, permissions

from .models import Task
from .serializers import TaskSerializer
# Create your views here.


class CreateTaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer


class ListTasksView(generics.ListAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer


class TaskRudView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
