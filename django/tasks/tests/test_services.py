import pytest
from django.core.exceptions import ValidationError
from ..services import assign_task
from ..models import Task
from ..tasks import send_assignment_email

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

