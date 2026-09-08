from crm_app.controllers import LoginController, RegisterController
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def login_page(request):
    return LoginController(request).form_page()

def register_page(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('home')
    return RegisterController(request).form_page()

def logout_page(request):
    return LoginController(request).logout()

