from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
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

class TaskCreateView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = TaskForm()
        return render(request, "task/create.html", {"form": form, "project": project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            task.type.set(form.cleaned_data['type'])
            return redirect("project-detail", pk=project.pk)
        return render(request, "task/create.html", {"form": form, "project": project})

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task/update.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        task = form.save()
        task.type.set(form.cleaned_data['type'])
        return redirect('detail', pk=task.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context


class TaskDeleteView(DeleteView):
    model = Task

    def get_object(self, queryset=None):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.project.pk})

    def get(self, request, *args, **kwargs):
        return redirect('project-detail', pk=self.get_object().project.pk)