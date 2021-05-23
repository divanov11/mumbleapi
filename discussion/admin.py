from django.contrib import admin
from .models import (Discussion, DiscussionComment, DiscussionVote)
from django.apps import apps

models = apps.get_models()

class AdminDiscussion(admin.ModelAdmin):
    list_display = ('headline', 'user', 'created',)
    search_fields = ('user',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'


class AdminDiscussionComment(admin.ModelAdmin):
    list_display = ('discussion', 'user', 'created',)
    search_fields = ('user',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'


class AdminDiscussionVote(admin.ModelAdmin):
    list_display = ('discussion', 'user', 'value',)
    search_fields = ('user',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'


admin.site.register(Discussion, AdminDiscussion)
admin.site.register(DiscussionComment, AdminDiscussionComment)
admin.site.register(DiscussionVote, AdminDiscussionVote)

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['id', 'headline', 'user', 'created']
    list_filter = ['user']
    search_fields = ['user', 'headline']
    ordering = ['-created']


@admin.register(DiscussionComment)
class DiscussionCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussion', 'user', 'created']
    list_filter = ['user']
    search_fields = ['user', 'discussion']
    ordering = ['-created']


@admin.register(DiscussionVote)
class DiscussionVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussion', 'user', 'created']
    list_filter = ['user']
    search_fields = ['user', 'discussion']
    ordering = ['-created']


for model in models:
    if admin.sites.AlreadyRegistered:
        pass
    else:
        admin.site.register(model)

# admin.site.register(Discussion)
# admin.site.register(DiscussionComment)
# admin.site.register(DiscussionVote)
