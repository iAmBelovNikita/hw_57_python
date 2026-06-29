from django.urls import path
from .views import (
    TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView, ProjectUsersView,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("project/new/", ProjectCreateView.as_view(), name="project-create"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path("project/<int:pk>/users/", ProjectUsersView.as_view(), name="project-users"),

    path("project/<int:pk>/task/new/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete"),
]