from crm_app.controllers.base import BaseController
from crm_app.forms import StatusForm
from crm_app.models import Status


class StatusController(BaseController):
    _CLASS_FORM = StatusForm
    _REDIRECT_PAGE = "status-list"
    _ENTITY_NAME = "статус"
    _ADDITIONAL_JS = ["statusCard"]
    _MODEL = Status

