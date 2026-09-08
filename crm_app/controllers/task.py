from django.shortcuts import redirect, get_object_or_404
from crm_app.controllers.base import BaseController
from crm_app.forms import TaskForm, CommentForm
from crm_app.models import Task
from crm_app.models import Comment

class TaskController(BaseController):
    _CLASS_FORM = TaskForm
    _ENTITY_NAME = "задачу"
    _MODEL = Task

    def _get_form_kwargs(self) -> dict:
        return {'user': self._request.user}

    def _form_submit(self) -> bool:
        form = self.form
        if not form.is_valid():
            return False

        old_task = None
        if self._entity_id is not None:
            old_task = Task.objects.get(pk=self._entity_id)

        old_communication_time = old_task.communication_time if old_task else None

        if not self._request.user.is_superuser:
            if old_task:
                form.instance.user = old_task.user
            else:
                form.instance.user = self._request.user

        form.save()
        new_communication_time = form.cleaned_data.get('communication_time')

        if old_task:
            comment_text = self._build_communication_change_comment(
                old_communication_time, new_communication_time
            )
            Comment.objects.create(
                task=form.instance,
                user=self._request.user if self._request.user.is_authenticated else None,
                text=comment_text
            )

        return True

    def _build_communication_change_comment(self, old_value, new_value):
        if old_value is None and new_value is not None:
            return f"Установлена дата связи: {new_value.strftime('%d.%m.%Y %H:%M')}"
        if old_value is not None and new_value is None:
            return f"Дата связи удалена (была {old_value.strftime('%d.%m.%Y %H:%M')})"
        if old_value is not None and new_value is not None:
            return (
                f"Дата связи изменена с {old_value.strftime('%d.%m.%Y %H:%M')} "
                f"на {new_value.strftime('%d.%m.%Y %H:%M')}"
            )
        return "Дата связи не изменена"

    def _before_form_save(self, form):
        pass

    def form_page(self):
        if self._request.method == 'POST' and 'comment_submit' in self._request.POST:
            return self._handle_comment_submit()

        if self._is_form_submitted():
            if self.model and self.model.id:
                return redirect('task_update', task_id=self.model.id)
            return redirect('user_tasks')

        return self._render_form_page()

    def _handle_comment_submit(self):
        if not self._entity_id:
            return redirect('task_create')
        task = get_object_or_404(Task, id=self._entity_id)
        comment_form = CommentForm(self._request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = self._request.user if self._request.user.is_authenticated else None
            comment.save()
        return redirect('task_update', task_id=self._entity_id)

    def _get_form_page_context(self) -> dict:
        context = super()._get_form_page_context()
        if self._entity_id:
            task = get_object_or_404(Task, id=self._entity_id)
            context['comments'] = task.comments.all()
            context['comment_form'] = CommentForm()
            context['task_id'] = self._entity_id
        return context