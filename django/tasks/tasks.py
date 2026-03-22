from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_assignment_email(task_id: int):
    from .models import Task
    
    task = Task.objects.select_related("assignee", "project").get(pk=task_id)
    
    if not task.assignee:
        return "No assignee, skipping"
    
    send_mail(
        subject=f"[{task.project.name}] You've been assigned: {task.title}",
        message=f"Task '{task.title}' has been assigned to you. Due: {task.due_date}",
        from_email="noreply@jira-clone.com",
        recipient_list=[task.assignee.email],
    )
    
    return f"Email sent to {task.assignee.email}"
