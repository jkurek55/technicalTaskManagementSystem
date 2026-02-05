from django.db import models

# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    is_terminal = models.BooleanField()
