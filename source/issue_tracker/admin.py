from django.contrib import admin
from .models import Task, Status, Type

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'summary', 'status', 'type', 'created_at', 'updated_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ('summary', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fields = (
        'summary',
        'description',
        'status',
        'type',
        'created_at',
        'updated_at',
    )


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Task, TaskAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)