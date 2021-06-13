from django.contrib import admin
from .models import Message


class AdminMessage(admin.ModelAdmin):
    search_fields = ('to_user',)
    list_filter = ('to_user',)
    empty_value_display = '-empty field-'


admin.site.register(Message, AdminMessage)
