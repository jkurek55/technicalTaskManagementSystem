import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpass123"
    )

@pytest.fixture
def status_open():
    from tasks.models import Status
    return Status.objects.create(name="Open", is_terminal=False)

@pytest.fixture
def status_terminal():
    from tasks.models import Status
    return Status.objects.create(name="Done", is_terminal=True)

@pytest.fixture
def project():
    from tasks.models import Project
    return Project.objects.create(name="Test Project")

@pytest.fixture
def task(project, status_open):
    from tasks.models import Task
    return Task.objects.create(
        title="Test Task",
        project=project,
        status=status_open,
    )

@pytest.fixture
def assigned_task(project, status_open, user):
    from tasks.models import Task
    return Task.objects.create(
        title="Test Task",
        project=project,
        status=status_open,
        assignee=user
    )

@pytest.fixture
def terminal_task(project, status_terminal):
    from tasks.models import Task
    return Task.objects.create(
        title="Test Task",
        project=project,
        status=status_terminal,
    )