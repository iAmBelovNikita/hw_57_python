from django.db import models

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

class Task(models.Model):
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    type = models.ForeignKey(Type, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)