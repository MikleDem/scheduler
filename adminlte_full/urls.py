from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.views import PasswordChangeView, LoginView, logout_then_login 
from . import views

urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),

    url(r'^message/(?P<id>\w+)$', views.index, name='adminlte_full_show_message'),
    url(r'^messages$', views.index, name='adminlte_full_all_messages'),

    url(r'^notification/(?P<id>\w+)$', views.index, name='adminlte_full_show_notification'),
    url(r'^notifications$', views.index, name='adminlte_full_all_notifications'),

    url(r'^task/(?P<id>\w+)$', views.index, name='adminlte_full_show_task'),
    url(r'^tasks$', views.index, name='adminlte_full_all_tasks'),

    url(
        r'^profile$',
        PasswordChangeView.as_view(template_name='adminlte_full/user/password_change_form.html'),
        name='adminlte_full_profile',
    ),

    url(
        r'^login$',
        LoginView.as_view(template_name='adminlte_full/user/login.html'),
        name='adminlte_full_login'
    ),

    url(
        r'^logout$',
        logout_then_login,
        {
            'login_url': '/'
        },
        name='adminlte_full_logout'
    ),
]
