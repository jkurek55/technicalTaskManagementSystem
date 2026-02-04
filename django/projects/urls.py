from django.urls import path
from .views import ProjectRudView, ProjectListGetView, ProjectCreateView

urlpatterns = [
    path("<int:pk>", ProjectRudView.as_view()),
    path("create", ProjectCreateView.as_view()),
    path("", ProjectListGetView.as_view())
]
