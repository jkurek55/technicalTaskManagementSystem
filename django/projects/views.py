from django.shortcuts import render
from rest_framework import generics, permissions
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
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
