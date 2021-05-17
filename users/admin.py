from django.contrib import admin

# Register your models here.
from .models import UserProfile, TopicTag

admin.site.register(UserProfile)
admin.site.register(TopicTag)
