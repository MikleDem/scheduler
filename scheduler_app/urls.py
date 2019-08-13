from django.conf.urls import url
from django.urls import path
from scheduler_app.views import my_view_1, TaskView, EditTaskView, delete


urlpatterns = [
    url(r'^$', my_view_1, name='index'),
    path('add_task/', TaskView.as_view()),
    path('edit_task/<int:task_id>/', EditTaskView.as_view()),
    path('delete_task/<int:task_id>/', delete, name='delete'),
]
