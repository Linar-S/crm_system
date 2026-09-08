from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .base import BaseController
from ..forms import LoginForm, RegisterForm


class LoginController(BaseController):
    _CLASS_FORM = LoginForm
    _REDIRECT_PAGE = "home"


    def _form_submit(self):
        username = self.form.cleaned_data["username"]
        password = self.form.cleaned_data["password"]

        user = authenticate(
            self._request,
            username=username,
            password=password
            )
        if user:
            login(self._request, user)
            return True

        return False

    def logout(self):
        logout(self._request)
        return redirect("login")

    def _get_form_page_context(self) -> dict:
        return {
                "form": self.form,
                "title": "Вход",
                "page_title": "Вход",
                "additional_text": None,
                "additional_link": "/register",
                "link_text": None,
                "btn_text": "Войти"

        }

class RegisterController(BaseController):
    _CLASS_FORM = RegisterForm
    _REDIRECT_PAGE = "login"

    def _get_form_page_context(self) -> dict:
        return {
            "form": self.form,
            "title": "Регистрация нового пользовтеля",
            "page_title": "Регистрация нового пользовтеля в системе",
            "additional_text": None,
            "additional_link": None,
            "link_text": None,
            "btn_text": "Зарегистрировать пользователя"

        }