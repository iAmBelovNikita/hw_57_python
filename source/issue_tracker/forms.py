from django import forms
from django.forms import TextInput, Textarea
from .models import Task, Status, Type


class TaskForm(forms.ModelForm):
    summary = forms.CharField(
        required=True,
        max_length=200,
        label="Summary",
        widget=TextInput(attrs={"class": "form-control"})
    )

    description = forms.CharField(
        required=False,
        label="Description",
        widget=Textarea(attrs={"class": "form-control", "rows": "5"})
    )

    status = forms.ModelChoiceField(
        required=True,
        label="Status",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    type = forms.ModelMultipleChoiceField(
        required=True,
        label="Type",
        queryset=Type.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    class Meta:
        model = Task
        fields = ["summary", "description", "status", "type"]