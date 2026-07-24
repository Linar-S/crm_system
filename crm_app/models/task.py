from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, PROTECT, SET_NULL
from phonenumber_field.modelfields import PhoneNumberField
from .status import Status

class Task(Model):
    title = CharField(max_length=100)
    name = CharField(max_length=50)
    phone = PhoneNumberField(blank=False, null=False, region='RU', max_length=12)
    status = ForeignKey(Status, on_delete=PROTECT)
    user = ForeignKey(User, on_delete=SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title