from django import forms


class StatisticsFilterForm(forms.Form):
    month = forms.ChoiceField(
        label="Месяц",
        required=False,
        choices=[],  # заполним в __init__
    )
    date_from = forms.DateField(
        label="С даты",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    date_to = forms.DateField(
        label="По дату",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, months_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month'].choices = [('', '— Все месяцы —')] + (months_choices or [])