# Generated by Django 2.2.1 on 2019-05-08 09:56

from django.db import migrations, models
import scheduler_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler_app', '0002_job_cron_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='cron_task',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[scheduler_app.validators.validate_5_segments_or_not]),
        ),
        migrations.AlterField(
            model_name='job',
            name='task_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
