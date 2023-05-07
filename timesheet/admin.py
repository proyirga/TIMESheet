from django.contrib import admin
from . models import Project, Entry, Task, Timesheet

admin.site.register(Project)
admin.site.register(Entry)
admin.site.register(Timesheet)
