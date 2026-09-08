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
        "username": "Имя пользователя",
        "email": "Электронная почта",
        "password1": "Пароль",
        "password2": "Повторите пароль",
    }

    email = forms.EmailField(required=True)
    is_superuser = forms.BooleanField(required=False, label="Руководитель")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_superuser"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        if commit:
            user.save()
        return user
        


