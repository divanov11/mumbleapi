from django.contrib import admin
from .models import Mumble, MumbleVote


class AdminMumble(admin.ModelAdmin):
    pass


class AdminMumbleVote(admin.ModelAdmin):
    pass


admin.site.register(Mumble, AdminMumble)
admin.site.register(MumbleVote, AdminMumbleVote)
