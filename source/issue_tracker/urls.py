from django.urls import path

from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path("", TaskListView.as_view(), name="list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/new/", TaskCreateView.as_view(), name="create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete"),
]