from django.forms import ModelForm
from django import forms
from .models import Job


class TaskForm(ModelForm):
    class Meta:
        model = Job
        fields = ['task', 'task_datetime', 'cron_task']

