from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from crm_app.forms.statistics import StatisticsFilterForm
from crm_app.models import Status, Task


@login_required
def success_statistics(request):
    successful_status = Status.objects.get(name='Успешный')
    refused_status = Status.objects.get(name='Отказ')

    # 1. Список месяцев, в которых есть закрытые задачи
    months_qs = (
        Task.objects
        .filter(closed_at__isnull=False)
        .annotate(month=TruncMonth('closed_at'))
        .values_list('month', flat=True)
        .distinct()
        .order_by('-month')
    )

    month_names_ru = [
        '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
    ]

    months_choices = [
        (m.strftime('%Y-%m'), f"{month_names_ru[m.month]} {m.year}")
        for m in months_qs
        if m is not None
    ]

    # 2. Форма
    form = StatisticsFilterForm(request.GET or None, months_choices=months_choices)

    # 3. Queryset для фильтрации по периоду закрытия
    closed_qs = Task.objects.filter(closed_at__isnull=False)

    selected_month = None
    date_from = None
    date_to = None

    if form.is_valid():
        selected_month = form.cleaned_data.get('month')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

    if selected_month:
        year, month = map(int, selected_month.split('-'))
        closed_qs = closed_qs.filter(closed_at__year=year, closed_at__month=month)

    if date_from:
        closed_qs = closed_qs.filter(closed_at__date__gte=date_from)
    if date_to:
        closed_qs = closed_qs.filter(closed_at__date__lte=date_to)

    # 4. Статистика по всем активным пользователям
    #    - total: ВСЕ заявки пользователя (без фильтра по периоду)
    #    - success / refused / total_amount: только закрытые в периоде
    stats = (
        User.objects
        .filter(is_active=True)
        .annotate(
            total=Count('task', distinct=True),
            success=Count(
                'task',
                filter=Q(task__in=closed_qs, task__status=successful_status),
                distinct=True,
            ),
            refused=Count(
                'task',
                filter=Q(task__in=closed_qs, task__status=refused_status),
                distinct=True,
            ),
            total_amount=Sum(
                'task__amount',
                filter=Q(task__in=closed_qs, task__status=successful_status),
            ),
        )
        .order_by('-total_amount')
    )

    # 5. Общие итоги
    #    total — по всем задачам (не фильтруется)
    #    success / refused / total_sum — по закрытым в периоде
    totals = {
        'total': Task.objects.count(),
        'success': closed_qs.filter(status=successful_status).count(),
        'refused': closed_qs.filter(status=refused_status).count(),
        'total_sum': (
            closed_qs
            .filter(status=successful_status)
            .aggregate(s=Sum('amount'))['s'] or 0
        ),
    }

    context = {
        'form': form,
        'stats': stats,
        'totals': totals,
        'selected_month': selected_month,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'statistics.html', context)