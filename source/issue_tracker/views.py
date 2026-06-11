from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Task
from .forms import TaskForm

# Create your views here.

class TaskListView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all().order_by('-created_at')
        return context

class TaskDetailView(TemplateView):
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return context

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, "create.html", {"form": form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect("detail", pk=task.pk)
        return render(request, "create.html", {"form": form})

class TaskUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        form = TaskForm(instance=self.task)
        return render(request, "update.html", {"form": form, "task": self.task})

    def post(self, request, pk):
        form = TaskForm(request.POST, instance=self.task)
        if form.is_valid():
            task = form.save()
            return redirect("detail", pk=task.pk)
        return render(request, "update.html", {"form": form, "task": self.task})