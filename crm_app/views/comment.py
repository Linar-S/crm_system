from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from crm_app.models import Comment
from crm_app.forms import CommentForm

@require_POST
@csrf_exempt
def add_comment_ajax(request, task_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task_id = task_id
        comment.user = request.user if request.user.is_authenticated else None
        comment.save()
        return JsonResponse({
            'success': True,
            'user': comment.user.username if comment.user else 'Аноним',
            'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
            'text': comment.text,
        })
    else:
        return JsonResponse({'success': False, 'errors': form.errors})