from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import render
from crm_app.models import Status, Task


@login_required
def success_statistics(request):
    successful_status = Status.objects.get(name='Успешный')
    refused_status = Status.objects.get(name='Отказ')

    # Статистика по каждому пользователю
    stats = (
        Task.objects
        .values('user__first_name', 'user__last_name', 'user__username')
        .annotate(
            total=Count('id'),
            success=Count('id', filter=Q(status=successful_status)),
            refused=Count('id', filter=Q(status=refused_status)),
            total_amount=Sum('amount', filter=Q(status=successful_status)),
        )
        .order_by('-total_amount')
    )

    totals = Task.objects.aggregate(
        total=Count('id'),
        success=Count('id', filter=Q(status=successful_status)),
        refused=Count('id', filter=Q(status=refused_status)),
        total_sum=Sum('amount', filter=Q(status=successful_status)),
    )

    context = {
        'stats': stats,
        'totals': totals,
    }
    return render(request, 'statistics.html', context)