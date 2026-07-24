from django.shortcuts import redirect, get_object_or_404
from crm_app.controllers.base import BaseController
from crm_app.forms import TaskForm, CommentForm
from crm_app.models import Task


class TaskController(BaseController):
    _CLASS_FORM = TaskForm
    _REDIRECT_PAGE = "status-list"
    _ENTITY_NAME = "задачу"
    _MODEL = Task

    def _get_form_kwargs(self) -> dict:

        return {'user': self._request.user}

    def _form_submit(self) -> bool:
        form = self.form
        if not form.is_valid():
            return False

        if not self._request.user.is_superuser:
            if self.model:
                form.instance.user = self.model.user
            else:
                form.instance.user = self._request.user

        form.save()
        return True

    def _before_form_save(self, form):

        pass

    def form_page(self):
        if self._request.method == 'POST' and 'comment_submit' in self._request.POST:
            return self._handle_comment_submit()

        if self._is_form_submitted():
            return redirect(self._REDIRECT_PAGE)

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