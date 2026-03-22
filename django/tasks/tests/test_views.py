import pytest
from django.urls import reverse
from ..models import Task

@pytest.mark.django_db
def test_create_task(authenticated_client, user, project, status_open):
    url = reverse("task-create")

    payload = {
        "title": "Fix bug",
        "priority": 2,
        "project": project.id,
        "status": status_open.id,
        "assignee": user.id
    }

    response = authenticated_client.post(
        url, payload, format="json"
    )

    assert response.status_code == 201

    task = Task.objects.get(pk=response.data["id"])
    assert task.title == "Fix bug"
    assert task.priority == 2
    assert task.project_id == project.id
    assert task.created_at
    assert task.created_by == user


@pytest.mark.django_db
def test_create_task_unauthenticated(api_client, project, status_open):
    url = reverse("task-create")

    payload = {
        "title": "Fix bug",
        "priority": 2,
        "project": project.id,
        "status": status_open.id
    }

    response = api_client.post(
        url, payload, format="json"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_task_missing_title(authenticated_client, project, status_open):
    url = reverse('task-create')

    payload = {
        "priority": 2,
        "project": project.id,
        "status": status_open.id
    }

    response = authenticated_client.post(
        url,
        payload,
        format="json"
    )

    assert response.status_code == 400