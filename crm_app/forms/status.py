from crm_app.forms.base import BaseForm
from crm_app.models import Status


class StatusForm(BaseForm):
    _LABEL_NAME = {
        "name":"Название",
    }

    class Meta:
        model = Status
        fields = "__all__"
