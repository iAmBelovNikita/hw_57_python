from django.core.exceptions import PermissionDenied


class ProjectMemberRequiredMixin:
    def get_project(self):
        raise NotImplementedError("Define get_project() on the view.")

    def has_project_access(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return self.get_project().users.filter(pk=user.pk).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_project_access():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)