from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Textarea
from .models import Task, Status, Type, Project


def validate_summary_min_length(value):
    if len(value.strip()) < 3:
        raise ValidationError('Summary should be minimum 3 characters long')

def validate_description_no_spam(value):
    forbidden = ['fuck', 'shit', 'shitfuck']
    for word in forbidden:
        if word.lower() in value.lower():
            raise ValidationError(f"Description shouldn't contain word: '{word}'")

class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="Title",
        widget=TextInput(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        required=True,
        label="Description",
        widget=Textarea(attrs={"class": "form-control", "rows": "5"}),
    )
    start_date = forms.DateField(
        required=True,
        label="Start date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    end_date = forms.DateField(
        required=False,
        label="End date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "end_date"]

class TaskForm(forms.ModelForm):
    summary = forms.CharField(
        required=True,
        max_length=200,
        label="Summary",
        widget=TextInput(attrs={"class": "form-control"}),
        validators=[validate_summary_min_length],
    )

    description = forms.CharField(
        required=False,
        label="Description",
        widget=Textarea(attrs={"class": "form-control", "rows": "5"}),
        validators=[validate_description_no_spam],
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