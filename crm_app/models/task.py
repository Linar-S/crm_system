from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, PROTECT, SET_NULL, PositiveIntegerField, DateTimeField
from phonenumber_field.modelfields import PhoneNumberField
from .status import Status
from django.utils import timezone
from django.core.exceptions import ValidationError

class Task(Model):
    title = CharField(max_length=100)
    name = CharField(max_length=50)
    phone = PhoneNumberField(blank=False, null=False, region='RU', max_length=12)
    status = ForeignKey(Status, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    amount = PositiveIntegerField(null=True, blank=True, default=None)
    communication_time = DateTimeField(null=True, blank=True, default=None)

    def clean(self):
        if self.communication_time and self.communication_time < timezone.now():
            raise ValidationError({'communication_time': 'Время коммуникации не может быть в прошлом.'})

    def __str__(self) -> str:
        return self.title