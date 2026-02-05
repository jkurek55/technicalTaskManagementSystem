from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>", views.StatusRudView.as_view()),
    path("create", views.StatusCreateView.as_view()),
    path("", views.StatusListGetView.as_view())
]

