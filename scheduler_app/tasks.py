from __future__ import absolute_import
import json
import pytz
from scheduler_2.celery import app
from celery.task.control import revoke
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import logging
import subprocess
from scheduler_app.models import Job


@app.task(ignore_result=True)
def run_job_id(job_id):
    job = Job.objects.get(id=job_id)
    if not job.cron_task:
        job.status = 'passed'
        job.save()
    
    logging.warning(f'Run task {job.task}')
    subprocess.run(job.task, shell=True, check=True)


def sync_task(job):
    if job.cron_task:
        minute, hour, day_of_week, day_of_month, month_of_year = job.cron_task.split(' ')
        schedule = CrontabSchedule.objects.create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
        )
        job.status = 'active'
        
        if job.periodic_task:
            old_crontab = job.periodic_task.crontab
            job.periodic_task.crontab = schedule
            job.periodic_task.save()

            old_crontab.delete()
        else:
            task = PeriodicTask.objects.create(
                crontab=schedule, 
                name=f'Run cron job for {job.id}', 
                task='scheduler_app.tasks.run_job_id', 
                args=json.dumps([job.id])
            )

            job.periodic_task = task
    elif job.status != 'passed':
        if job.task_key:
            revoke(job.task_key, terminate=True)
        
        task_datetime = job.task_datetime.replace(tzinfo=pytz.UTC)
        job.task_key = run_job_id.apply_async((job.id, ), eta=task_datetime)
        job.status = 'active'
