from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.user_login);
admin.site.register(models.user_data);
admin.site.register(models.bubl_template);
admin.site.register(models.bubl_schedule);
admin.site.register(models.bubl_month_schedule);