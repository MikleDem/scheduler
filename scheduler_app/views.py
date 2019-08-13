from adminlte_full.menu import MenuItem, Menu
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Job
from .forms import TaskForm


class TaskView(View):
    template_name = 'add_task.html'

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task_data = Job(task=form.cleaned_data['task'], task_datetime=form.cleaned_data['task_datetime'],
                            cron_task=form.cleaned_data['cron_task'], user=request.user)
            task_data.save()
            return redirect(my_view_1)
        return render(request, self.template_name, {'form': form})


class EditTaskView(View):
    template_name = 'add_task.html'

    def get(self, request, task_id):
        task = Job.objects.get(id=task_id)
        form = TaskForm(instance=task)
        context = {
            'form': form,
            'task_id': task_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, task_id):
        task = Job.objects.get(id=task_id)
        form = TaskForm(data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(my_view_1)
        
        context = {
            'form': form,
            'task_id': task_id,
        }
        return render(request, self.template_name, context)


def delete(request, task_id):
    try:
        task = Job.objects.get(id=task_id)
        task.delete()
        return redirect(my_view_1)
    except Job.DoesNotExist:
        return render("<h2>Task not found</h2>")


@login_required
def my_view_1(request):
    cron_list = Job.objects.filter(user=request.user)
    context = {'cron_list': cron_list}
    return render(request, 'tasks_list.html', context)


def my_menuitems_builder(sender, **kwargs):
    # sender is an instance of Menu class
    single_menuitem_1 = MenuItem(1, 'Crons', 'index')
    sender.add_item(single_menuitem_1)


Menu.show_signal.connect(my_menuitems_builder)
