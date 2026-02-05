from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListTasksView.as_view()),
    path("<int:pk>", views.TaskRudView.as_view()),
    path("create", views.CreateTaskView.as_view()),
]

