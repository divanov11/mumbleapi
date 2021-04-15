from django.contrib import admin
from .models import Post, UserProfile, PostVote
# Register your models here.


admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(PostVote)