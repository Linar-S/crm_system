from django.shortcuts import render
from .status import status_list, status_form, status_delete
from .auth import login_page, register_page, logout_page
from .task import *
from .statistic import *
from ..models import Task


# Create your views here.
def home(request):
    return render(request, "home.html",
                  {
                    "title": "CRM - Система",
                    "tasks": Task.objects.all(),
                    "task_list": "Все задачи",
                  })