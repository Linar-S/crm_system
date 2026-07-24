from django.contrib import admin

from crm_app.models import Status, Task, Comment


# Register your models here.
admin.site.register(Status)
admin.site.register(Task)
admin.site.register(Comment)