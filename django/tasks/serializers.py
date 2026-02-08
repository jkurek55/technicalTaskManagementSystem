from rest_framework import serializers

from .models import Task
from projects.serializers import ProjectSerializer
from statuses.serializers import StatusSerializer
from users.serializers import UserReadSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskReadSerializer(serializers.ModelSerializer):
        project = ProjectSerializer()
        status = StatusSerializer()
        assignee = UserReadSerializer()
        created_by = UserReadSerializer()

        class Meta:
            model = Task
            fields = "__all__"
