from django.forms import ValidationError

from .models import Task, Project
from django.contrib.auth.models import AbstractBaseUser
import datetime
from django.db.models import F
from .tasks import send_assignment_email

def assign_task(*, task: Task, user: AbstractBaseUser):
    if task.status.is_terminal:
        raise ValidationError("Cannot assign a completed task.")
    if task.assignee==user:
        raise ValidationError("User already assigned")
    task.assignee = user
    task.save()
    
    send_assignment_email.delay(task.id)

    return task



def escalate_overdue_tasks(project: Project):
    tasks = Task.objects.filter(
        project=project,
        due_date__lt=datetime.datetime.now(),
        status__is_terminal=False,
    )
    updated = tasks.update(priority=F("priority") + 1)
    return updated


