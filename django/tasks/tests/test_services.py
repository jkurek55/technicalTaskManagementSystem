import pytest
from django.core.exceptions import ValidationError

from ..services import assign_task, escalate_overdue_tasks
from ..models import Task
from .factories import TaskFactory
from ..tasks import send_assignment_email
from unittest.mock import call
from datetime import timedelta 
from django.utils import timezone

@pytest.mark.django_db
def test_assign_task(user, task):

    result = assign_task(user=user, task=task)

    assert result.assignee == user


@pytest.mark.django_db
def test_user_already_assigned_exception(user, task):

    assign_task(user=user, task=task)

    with pytest.raises(ValidationError, match="User already assigned"):
        assign_task(user=user, task=task)


@pytest.mark.django_db
def test_already_completed(user, terminal_task):

    with pytest.raises(ValidationError, match="Cannot assign a completed task"):
        assign_task(user=user, task=terminal_task)


@pytest.mark.django_db
def test_assign_task_sens_email(mocker, task, user):

    mock_task = mocker.patch("tasks.services.send_assignment_email")

    assign_task(task=task, user=user)

    mock_task.delay.assert_called_once_with(task.id)

    #mock_task.delay.assert_not_called()


@pytest.mark.django_db
def test_assign_task_does_not_send_email_if_already_assigned(mocker, assigned_task, user):
    mock_task = mocker.patch("tasks.services.send_assignment_email")

    with pytest.raises(ValidationError, match="User already assigned"):
        assign_task(user=user, task=assigned_task)

    mock_task.delay.assert_not_called()


@pytest.mark.django_db
def test_assign_task_does_not_send_email_if_terminal(mocker, user, terminal_task):
    mock_task = mocker.patch("tasks.services.send_assignment_email")

    with pytest.raises(ValidationError, match="Cannot assign a completed task"):
        assign_task(user=user, task=terminal_task)

    mock_task.delay.assert_not_called()

@pytest.mark.django_db
@pytest.mark.bang
def test_assign_user_to_ten_tasks(mocker, user, project, status_open):
    mock_task = mocker.patch("tasks.services.send_assignment_email")

    tasks = TaskFactory.create_batch(10, project=project, status=status_open, priority=2)

    for task in tasks:
        assign_task(task=task, user=user)

    mock_task.delay.assert_has_calls([
        call(task.id) for task in tasks
    ])


@pytest.mark.parametrize("input,expected", [
    (0,1),
    (1,2),
    (3,4)
])
@pytest.mark.django_db
def test_escalate_priority(input, expected, project, status_open):
    task = TaskFactory(
        priority=input, 
        project=project, 
        status=status_open,
        due_date=timezone.now() - timedelta(days=1)
        )
    escalate_overdue_tasks(project)
    task.refresh_from_db()

    assert task.priority == expected

