from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse
from ..models import Task, Project
from ..forms import TaskForm


class TaskDetailView(DetailView):
    model = Task
    template_name = "task/detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task/create.html"
    context_object_name = "task"

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect(self.get_success_url())

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/update.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        task = form.save()
        return redirect('detail', pk=task.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.pk})

    def get(self, request, *args, **kwargs):
        return redirect('project-detail', pk=self.get_object().project.pk)