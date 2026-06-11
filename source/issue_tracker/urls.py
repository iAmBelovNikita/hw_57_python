from django.urls import path

from .views import TaskListView, TaskDetailView, TaskCreateView

urlpatterns = [
    path("", TaskListView.as_view(), name="list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/new/", TaskCreateView.as_view(), name="create"),
]