from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Count, F


closed_tasks_last_month = Task.objects.filter(
    status__name="Done",
    updated_at__gte=timezone.now() - timedelta(days=30)
)

tasks_by_status_and_type = Task.objects.filter(
    Q(status__name="New") | Q(status__name="In Progress"),
    Q(type__name="Bug")  | Q(type__name="Task")
).distinct()

open_tasks_with_bug = Task.objects.filter(
    ~Q(status__name="Done"),
).filter(
    Q(summary__icontains="bug") | Q(type__name="Bug")
).distinct()

tasks_fields_only = Task.objects.values(
    "id",
    "summary",
    "type__name",
    "status__name"
)

tasks_summary_equals_description = Task.objects.filter(
    summary=F("description")
)

tasks_count_by_type = Type.objects.annotate(
    task_count=Count("tasks")
).values("name", "task_count")