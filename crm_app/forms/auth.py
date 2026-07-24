from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crm_app.forms.base import BaseForm


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )



class RegisterForm(UserCreationForm, BaseForm):
    _LABEL_NAME = {
        "username":"Имя пользователя",
        "email":"Электронная почта",
        "password1":"Пароль",
        "password2": "Повторите пароль",
    }

    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",]
        


