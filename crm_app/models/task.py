from django.contrib.auth.models import User
from django.db.models import (
    Model, CharField, ForeignKey, PROTECT, SET_NULL,
    PositiveIntegerField, DateTimeField,
)
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError

from .status import Status


class Task(Model):
    title = CharField(max_length=100)
    name = CharField(max_length=50)
    phone = PhoneNumberField(blank=False, null=False, region='RU', max_length=12)
    status = ForeignKey(Status, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    amount = PositiveIntegerField(null=True, blank=True, default=None)
    communication_time = DateTimeField(null=True, blank=True, default=None)

    created_at = DateTimeField(default=timezone.now, verbose_name="Дата создания")
    closed_at = DateTimeField(null=True, blank=True, verbose_name="Дата закрытия")

    def clean(self):
        if self.communication_time and self.communication_time < timezone.now():
            raise ValidationError({'communication_time': 'Время коммуникации не может быть в прошлом.'})

    def save(self, *args, **kwargs):
        FINAL_STATUSES = ['Успешный', 'Отказ']

        if self.status and self.status.name in FINAL_STATUSES + ['Спам']:
            self.communication_time = None

        if self.status and self.status.name in FINAL_STATUSES:
            if self.closed_at is None:
                self.closed_at = timezone.now()
        else:
            self.closed_at = None

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title