import factory
from django.contrib.auth import get_user_model
from tasks.models import Task, Project, Status

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Project {n}")


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.Sequence(lambda n: f"Status {n}")
    is_terminal = False


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: f"Task {n}")
    priority = 1
    project = factory.SubFactory(ProjectFactory)
    status = factory.SubFactory(StatusFactory)
    assignee = None
    created_by = factory.SubFactory(UserFactory)