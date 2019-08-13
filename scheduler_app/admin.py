from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'task_datetime', 'cron_task', 'user', 'periodic_task', 'task_key', 'status')
    list_filter = ('status', )


admin.site.register(Job, JobAdmin)
