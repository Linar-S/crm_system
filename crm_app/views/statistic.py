from django.db.models import Sum
from django.shortcuts import render
from crm_app.models import Task, Status

def success_statistics(request):
    successful_status = Status.objects.get(name='Успешный')
    stats = (
        Task.objects
        .filter(status=successful_status)
        .values('user__username')
        .annotate(total_amount=Sum('amount'))
        .order_by('-total_amount')
    )
    total_sum = Task.objects.filter(status=successful_status).aggregate(Sum('amount'))['amount__sum']
    context = {
        'stats': stats,
        'total_sum': total_sum,
    }
    return render(request, 'statistics.html', context)