from django.contrib import admin

from core.models import Company, Invite, Project, Task, User

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Invite)