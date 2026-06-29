from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'type'

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'status'

class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='projects', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'project'
        permissions = [
            ("manage_project_users", "Can manage project users"),
        ]

class Task(models.Model):
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    type = models.ManyToManyField(Type, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary

    class Meta:
        db_table = 'task'