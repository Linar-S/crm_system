from django import forms
from crm_app.forms.base import BaseForm
from crm_app.models.task import Task

class TaskForm(BaseForm):
    _LABEL_NAME = {
        "title": "Заголовок",
        "name": "Имя",
        "phone": "номер телефона",
        "status": "статус задачи",
        "user": "ответственный"
    }

    class Meta:
        model = Task
        fields = ["title", "name", "phone", "status", "user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields.pop('user', None)