# projects/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Task
from projects.models import Project
from statuses.models import Status

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with test data'

    def handle(self, *args, **kwargs):
        # Create users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user_{i}',
                defaults={'email': f'user_{i}@example.com'}
            )
            if created:
                user.set_password('password')
                user.save()
            users.append(user)

        # Create statuses
        statuses = []
        for name, is_terminal in [
            ('To Do', False),
            ('In Progress', False),
            ('In Review', False),
            ('Done', True),
            ('Cancelled', True)
        ]:
            status, _ = Status.objects.get_or_create(
                name=name,
                defaults={'is_terminal': is_terminal}
            )
            statuses.append(status)

        # Create projects
        projects = []
        for i in range(5):
            project, _ = Project.objects.get_or_create(
                name=f'Project {i}',
                defaults={'description': f'Description for project {i}'}
            )
            projects.append(project)

        # Create tasks
        for i in range(50):
            Task.objects.get_or_create(
                title=f'Task {i}',
                defaults={
                    'description': f'Description for task {i}',
                    'project': projects[i % len(projects)],
                    'status': statuses[i % len(statuses)],
                    'assignee': users[i % len(users)],
                    'created_by': users[(i + 1) % len(users)],
                    'priority': i % 4,
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f'Created {User.objects.count()} users, '
            f'{Project.objects.count()} projects, '
            f'{Status.objects.count()} statuses, '
            f'{Task.objects.count()} tasks'
        ))