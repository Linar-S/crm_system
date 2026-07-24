from django.urls import path
from crm_app import views


status_urls = [
    path("status/list/", views.status_list, name="status-list"),
    path("status/add/", views.status_form, name="status-add"),
    path("status/update/<int:status_id>/", views.status_form, name="status-update"),
    path("status/delete/<int:status_id>/", views.status_delete, name="status-delete"),


]
