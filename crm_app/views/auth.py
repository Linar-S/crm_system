from crm_app.controllers import LoginController, RegisterController

def login_page(request):
    return LoginController(request).form_page()

def register_page(request):
    return RegisterController(request).form_page()

def logout_page(request):
    return LoginController(request).logout()

