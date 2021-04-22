from django.contrib import admin

# Register your models here.

from .models import Mumble, MumbleVote


admin.site.register(Mumble)
admin.site.register(MumbleVote)
