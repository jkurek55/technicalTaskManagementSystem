import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .factories import UserFactory, ProjectFactory, StatusFactory, TaskFactory

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
    return UserFactory()

@pytest.fixture
def project():
    return ProjectFactory()

@pytest.fixture
def status_open():
    return StatusFactory(is_terminal=False)

@pytest.fixture
def status_terminal():
    return StatusFactory(is_terminal=True)

@pytest.fixture
def task(project, status_open):
    return TaskFactory(project=project, status=status_open)

@pytest.fixture
def terminal_task(project, status_terminal):
    return TaskFactory(project=project, status=status_terminal)

@pytest.fixture
def assigned_task(project, status_open, user):
    return TaskFactory(project=project, status=status_open, assignee=user)