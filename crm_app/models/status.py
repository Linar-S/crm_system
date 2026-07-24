from django.db.models import Model, CharField


class Status(Model):
    name = CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name