from django.contrib import admin
from datetime import timedelta
from .models import Mumble, MumbleVote


class AdminMumble(admin.ModelAdmin):
    list_display = ('user', 'vote_rank', 'created','get_utc')
    search_fields = ('user',)
    list_filter = ('created', 'vote_rank', 'user',)
    empty_value_display = '-empty field-'

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'



class AdminMumbleVote(admin.ModelAdmin):
    list_display = ('user', 'mumble', 'value')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-empty field-'


admin.site.register(Mumble, AdminMumble)
admin.site.register(MumbleVote, AdminMumbleVote)
