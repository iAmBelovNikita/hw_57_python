from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from ..models import Project
from ..forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = "project/index.html"
    context_object_name = "projects"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.task_set.all().order_by("-created_at")
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/create.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/update.html"

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("project-list")

    def get(self, request, *args, **kwargs):
        return redirect("project-list")


class ProjectUsersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["pk"])
        return self.render_page(request, project)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs["pk"])
        action = request.POST.get("action")
        user = get_object_or_404(User, pk=request.POST.get("user_id"))
        if action == "add":
            project.users.add(user)
        elif action == "remove":
            project.users.remove(user)
        return redirect("project-users", pk=project.pk)

    def render_page(self, request, project):
        members = project.users.all()
        available = User.objects.exclude(pk__in=members.values("pk"))
        context = {"project": project, "members": members, "available": available}
        return render(request, "project/users.html", context)