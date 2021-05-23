from django.contrib import admin
from .models import Discussion, DiscussionComment, DiscussionVote


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
