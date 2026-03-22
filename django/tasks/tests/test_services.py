import pytest
from django.core.exceptions import ValidationError
from ..services import assign_task
from ..models import Task

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

