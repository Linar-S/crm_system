from django.urls import path
from crm_app.views.task import *

app_name = 'crm_app'

urlpatterns = [
    path('task/create/', task_form, name='task_create'),
    path('task/<int:task_id>/', task_form, name='task_update'),
    path('task/<int:task_id>/delete/', task_delete, name='task_delete'),
    path('task/<int:task_id>/status/', update_task_status, name='update_status'),
    path('api/task/<int:task_id>/update-status/', update_task_status, name='task-status-update'),
    path('task/my-tasks/', user_tasks, name='user_tasks'),
    path('task/overdue/', user_overdue, name='user_overdue'),
]