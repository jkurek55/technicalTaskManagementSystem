
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection, reset_queries
from django.db.models import Q, Avg, Count, F, FloatField, Max
from django.db.models.functions import Cast
from django.core.cache import cache
from django.db.models import Prefetch
from django.contrib.auth import get_user_model


from rest_framework import generics, permissions


from .models import Task, Status, Project
from django.contrib.auth import get_user_model
from .serializers import TaskSerializer, TaskReadSerializer
# Create your views here.


class CreateTaskView(generics.CreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

class ListTasksView(generics.ListAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskReadSerializer


class TaskRudView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskReadSerializer
        return TaskSerializer


def task_list_n1(request):
    reset_queries()

    latest_open_qs = Task.objects.filter(
        status__is_terminal=False
    ).order_by("-created_at").select_related("status")

    projects = Project.objects.prefetch_related(
        Prefetch("tasks", queryset=latest_open_qs, to_attr="latest_open_task")
    ).annotate(
        task_count=Count("tasks"),
        overdue=Count(
            "tasks",
            filter=Q(
                tasks__due_date__lt=datetime.datetime.now(),
                tasks__status__is_terminal=False,
            )
        ),
    )

    top_assignees = (
        Task.objects
        .filter(
            status__is_terminal=False,
            assignee__isnull=False,
        )
        .values("project_id", "assignee__username")
        .annotate(open_count=Count("id"))
        .order_by("project_id", "-open_count")
    )

    top_assignee_map = {}
    for row in top_assignees:
        pid = row["project_id"]
        if pid not in top_assignee_map:
            top_assignee_map[pid] = row["assignee__username"]

    report = []

    for project in projects:
        total = project.task_count
        if not total:
            continue

        latest_open = project.latest_open_task[0] if project.latest_open_task else None

        report.append({
            "project":      project.name,
            "total_tasks":  total,
            "overdue_rate": round(project.overdue / total, 2),
            "top_assignee": top_assignee_map.get(project.id),
            "latest_open":  latest_open.title if latest_open else None,
        })

    query_count = len(connection.queries)
    return JsonResponse({
        "query_count": query_count,
        "report": report
    })