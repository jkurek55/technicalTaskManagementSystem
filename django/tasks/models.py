from django.db import models
from django.db.models import PROTECT, CASCADE, SET_NULL

from statuses.models import Status
from projects.models import Project
from django.conf import settings


# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=CASCADE)
    status = models.ForeignKey(Status, on_delete=PROTECT)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
        null=True,
        blank=True,
        related_name="tasks_assigned"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        related_name="tasks_created",
        null=True
    )
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
