from django.contrib import admin
from .models import (Discussion,DiscussionComment,DiscussionVote)


admin.site.register(Discussion)
admin.site.register(DiscussionComment)
admin.site.register(DiscussionVote)
