from django.contrib import admin

# Register your models here.
from .models import TopicTag, SkillTag, UserProfile

admin.site.register(TopicTag)
admin.site.register(SkillTag)
admin.site.register(UserProfile)
