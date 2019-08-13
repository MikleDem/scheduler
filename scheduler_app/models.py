from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_5_segments_or_not
from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask
from django.dispatch import receiver


class Job(models.Model):
    STATUSES = (
        ('new', 'New'),
        ('active', 'Active'),
        ('passed', 'Passed'),
    )

    task = models.TextField(max_length=100)
    task_datetime = models.DateTimeField(blank=True, null=True)
    cron_task = models.CharField(max_length=50, validators=[validate_5_segments_or_not], blank=True, null=True)

    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True, on_delete=models.CASCADE)
    task_key = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, default=STATUSES[0][0], choices=STATUSES)

    user = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.task

    def save(self, *args, **kwargs):
        from scheduler_app.tasks import sync_task
        is_edit = bool(self.id)
        if is_edit:
            sync_task(self)

        result = super().save(*args, **kwargs)

        if not is_edit:
            sync_task(self)
            self.save()

    def clean(self):
        if self.task_datetime and self.cron_task:
            raise ValidationError("Sorry, you can add task datetime or cron task")
        elif not self.task_datetime and not self.cron_task:
            raise ValidationError("Please, add a task datetime or cron task")
