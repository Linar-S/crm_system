from django.urls import path
from crm_app import views
from .status import status_urls
from .auth import auth_urls
from .task import urlpatterns as task_urls

urlpatterns = [
    path("", views.home, name="home"),
    *status_urls,
    *auth_urls,
    *task_urls,

]
