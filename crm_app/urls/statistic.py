from django.urls import path
from crm_app import views

urlpatterns = [
    path('statistics/success/', views.success_statistics, name='success_statistics'),
]