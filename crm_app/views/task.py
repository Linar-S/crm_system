import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from crm_app.controllers import TaskController
from crm_app.models import Status, Task


@login_required(login_url='/login/')
def task_form(request, task_id: int | None = None):
    return TaskController(request, task_id).form_page()


@login_required(login_url='/login/')
def task_delete(request, task_id: int):
    return TaskController(request, task_id).delete()


@require_http_methods(["PATCH"])
@login_required(login_url='/login/')
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Проверка прав: суперпользователь или владелец задачи
    if not request.user.is_superuser and task.user != request.user:
        return JsonResponse({'success': False, 'error': 'Нет доступа'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Некорректный JSON'}, status=400)

    new_status_id = data.get('status')
    if not new_status_id:
        return JsonResponse({'success': False, 'error': 'Не указан статус'}, status=400)

    if not Status.objects.filter(id=new_status_id).exists():
        return JsonResponse({'success': False, 'error': 'Статус не найден'}, status=404)

    task.status_id = new_status_id
    task.save()  # здесь сработает логика closed_at из модели

    return JsonResponse({
        'success': True,
        'new_status': new_status_id,
        'closed_at': task.closed_at.isoformat() if task.closed_at else None,
    })


@login_required(login_url='/login/')
def user_tasks(request):
    tasks = Task.objects.filter(user=request.user).select_related('status', 'user')
    context = {
        'tasks': tasks,
        'task_list': 'Мои задачи',
    }
    return render(request, 'user_tasks.html', context)


@login_required(login_url='/login/')
def user_overdue(request):
    now = timezone.now()

    filter_conditions = Q(communication_time__isnull=False, communication_time__lt=now)

    if not request.user.is_superuser:
        filter_conditions &= Q(user=request.user)

    tasks = (
        Task.objects
        .filter(filter_conditions)
        .exclude(status__name__in=['Успешный', 'Спам', 'Отказ'])
        .select_related('status', 'user')
        .order_by('communication_time')
    )

    context = {
        'tasks': tasks,
        'overdue_list': 'Просроченные задачи',
    }
    return render(request, 'user_tasks.html', context)