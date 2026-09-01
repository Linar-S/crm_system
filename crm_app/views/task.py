from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from crm_app.controllers import TaskController
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from crm_app.models import Task
import json

@login_required(login_url='/login/')
def task_form(request, task_id: int | None = None):
    return TaskController(request, task_id).form_page()

def task_delete(request, task_id: int):
    return TaskController(request, task_id).delete()

@require_http_methods(["PATCH"])
@csrf_exempt
def update_task_status(request, task_id):
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        new_status_id = data.get('status')
        task.status_id = new_status_id
        task.save()
        return JsonResponse({'success': True, 'new_status': new_status_id})

@login_required
def user_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
        'task_list': 'Мои задачи',
    }
    return render(request, 'user_tasks.html', context)

@login_required
def user_overdue(request):
    now = timezone.now()

    filter_conditions = Q(communication_time__isnull=False, communication_time__lt=now)

    if not request.user.is_superuser:
        filter_conditions &= Q(user=request.user)

    tasks = Task.objects.filter(filter_conditions)
    tasks = tasks.exclude(status__name__in=['Успешный', 'Спам', 'Отказ'])
    tasks = tasks.order_by('communication_time')

    context = {
        'tasks': tasks,
        'overdue_list': 'Просроченные задачи',
    }
    return render(request, 'user_tasks.html', context)