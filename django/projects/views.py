from django.shortcuts import render
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.


class ProjectListGetView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    filterset_fields = ["name"]
    ordering_fields = ["created_at", "name"]
    search_fields = ["name", "description"]


class ProjectRudView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
