from django.urls import path

from crm_app.views import login_page, logout_page, register_page

auth_urls = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),

]

