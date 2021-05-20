from django.contrib import admin
from .models import Discussion, DiscussionComment, DiscussionVote


class AdminDiscussion(admin.ModelAdmin):
    pass


class AdminDiscussionComment(admin.ModelAdmin):
    pass


class AdminDiscussionVote(admin.ModelAdmin):
    pass


admin.site.register(Discussion, AdminDiscussion)
admin.site.register(DiscussionComment, AdminDiscussionComment)
admin.site.register(DiscussionVote, AdminDiscussionVote)
