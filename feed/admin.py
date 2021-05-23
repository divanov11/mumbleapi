from django.contrib import admin
from .models import Mumble, MumbleVote


class AdminMumble(admin.ModelAdmin):
    list_display = ('user', 'vote_rank', 'created',)
    search_fields = ('user',)
    list_filter = ('created', 'vote_rank', 'user',)
    empty_value_display = '-empty field-'



class AdminMumbleVote(admin.ModelAdmin):
    list_display = ('user', 'mumble', 'value',)
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-empty field-'


admin.site.register(Mumble, AdminMumble)
admin.site.register(MumbleVote, AdminMumbleVote)
