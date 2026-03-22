from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from .tasks import notify_task_assigned

@receiver(post_save, sender=Task)
def on_task_saved(sender, instance, created, **kwargs):
    # Only notify if assignee exists and was just assigned
    if instance.assignee:
        return notify_task_assigned.delay(instance.id, instance.assignee_id)

    