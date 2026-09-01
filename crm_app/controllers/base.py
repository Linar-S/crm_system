from functools import cached_property

from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest
from django.shortcuts import render, redirect


class BaseController:
    _CLASS_FORM: type[ModelForm]
    _REDIRECT_PAGE: str = ""
    _MODEL: type[Model] | None = None
    _ENTITY_NAME: str
    _ADDITIONAL_JS: list[str] = []

    def __init__(self, request: HttpRequest, entity_id: int | None = None) -> None:
        self._request: HttpRequest = request
        self._is_post: bool = request.method == "POST"
        self._entity_id: int | None = entity_id

    @cached_property
    def model(self) -> Model | None:
        if not self._MODEL or not self._entity_id:
            return None
        try:
         return self._MODEL.objects.get(pk=self._entity_id)
        except Exception:
            return None

    @cached_property
    def form(self) -> ModelForm | None:
        if self._is_post:
            if self.model:
                return self._CLASS_FORM(self._request.POST, instance=self.model, **self._get_form_kwargs())
            form = self._CLASS_FORM(self._request.POST, **self._get_form_kwargs())
            self._before_form_save(form)
            return form

        if self.model:
            return self._CLASS_FORM(instance=self.model, **self._get_form_kwargs())

        if self._entity_id:
            return None

        return self._CLASS_FORM(**self._get_form_kwargs())



    def form_page(self):
        if self._is_form_submitted():
            return redirect(self._REDIRECT_PAGE)

        return self._render_form_page()

    def delete(self):
        if self.model:
            self.model.delete()

        return redirect(self._REDIRECT_PAGE)

    def _is_form_submitted(self) -> bool:
        if not self._is_post or not self.form.is_valid():
            return False

        return self._form_submit()

    def _form_submit(self) -> bool:
        self.form.save()

        return True


    def _render_form_page(self):
        if not self.form:
            return redirect(self._REDIRECT_PAGE)



        return render(
            self._request,
            "form.html",
            self._get_form_page_context(),
        )

    def _get_form_page_context(self) -> dict:
        action_prefix: str = "Добавить" if not self._entity_id else "Изменить"
        return {
                "form": self.form,
                "title": f"{action_prefix} {self._ENTITY_NAME}",
                "page_title": f"{action_prefix} {self._ENTITY_NAME}",
                "btn_text": action_prefix,
                "additional_js": self._ADDITIONAL_JS
            }
    def _get_form_kwargs(self) -> dict:

        return {}

    def _before_form_save(self, form):
        ...




