from django.contrib import admin
from .models import Notification


class AdminNotification(admin.ModelAdmin):
    pass


admin.site.register(Notification, AdminNotification)
