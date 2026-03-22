from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import Project
from django.core.cache import cache
from tasks.models import Task

CACHE_KEY = 'project_task_list'

@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
def invalidate_cache_on_project_change(sender, **kwargs):
    cache.delete(CACHE_KEY)


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def invalidate_on_task_change(sender, **kwargs):
    cache.delete(CACHE_KEY)
