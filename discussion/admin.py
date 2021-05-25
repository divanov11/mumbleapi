from django.contrib import admin
from datetime import timedelta
from .models import (Discussion, DiscussionComment, DiscussionVote)
from django.apps import apps

models = apps.get_models()



@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['id', 'headline', 'user', 'get_utc']
    list_filter = ['user']
    search_fields = ['user', 'headline']
    ordering = ['-created']

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


@admin.register(DiscussionComment)
class DiscussionCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussion', 'user', 'get_utc']
    list_filter = ['user']
    search_fields = ['user', 'discussion']
    ordering = ['-created']

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


@admin.register(DiscussionVote)
class DiscussionVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussion', 'user', 'get_utc']
    list_filter = ['user']
    search_fields = ['user', 'discussion']
    ordering = ['-created']

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


for model in models:
    if admin.sites.AlreadyRegistered:
        pass
    else:
        admin.site.register(model)

# admin.site.register(Discussion)
# admin.site.register(DiscussionComment)
# admin.site.register(DiscussionVote)
