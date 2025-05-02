from django.contrib import admin

from persons.models import Persons, TaskLog

admin.site.register(Persons)
admin.site.register(TaskLog)
