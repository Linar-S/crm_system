from django.forms import Form, ModelForm
from django.forms.widgets import TextInput


class BaseForm(ModelForm):
    _LABEL_NAME: dict[str, str] = {}
    _CUSTOM_CLASS: dict[str, str] = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.help_text = ""

            if field_name in self._CUSTOM_CLASS:
                field.widget = TextInput(attrs={"class": self._CUSTOM_CLASS[field_name]})

            if field_name in self._LABEL_NAME:
                field.label = self._LABEL_NAME[field_name]
