from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.UserLogin)
admin.site.register(models.UserData)
admin.site.register(models.BublTemplate)
admin.site.register(models.BublSchedule)
admin.site.register(models.BublMonthSchedule)