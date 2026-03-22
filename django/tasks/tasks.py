from celery import shared_task

@shared_task
def notify_task_assigned(task_id, assignee_id):
    # Import models inside the function — not at the top
    # This avoids circular imports and app registry issues
    from tasks.models import Task
    from django.contrib.auth import get_user_model
    User = get_user_model()

    task = Task.objects.select_related('project', 'status').get(pk=task_id)
    assignee = User.objects.get(pk=assignee_id)

    # Simulating email — just print to console for now
    print(f"""
    ================================
    NOTIFICATION EMAIL
    To: {assignee.email}
    Subject: You have been assigned to a task
    
    Hi {assignee.username},
    You have been assigned to task: {task.title}
    Project: {task.project.name}
    Status: {task.status.name}
    ================================
    """)

    return f'Notification sent to {assignee.username}'
