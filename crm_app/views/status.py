from django.shortcuts import render

from crm_app.controllers import StatusController
from crm_app.models import Status


def status_list(request):

    statuses = Status.objects.prefetch_related('task_set').all()
    return render(request, "status/list.html", {
        "title": "Канбан-доска",
        "statuses": statuses,
    })

def status_form(request, status_id: int | None = None):
    return StatusController(request, status_id).form_page()

def status_delete(request, status_id: int):
    return StatusController(request, status_id).delete()

