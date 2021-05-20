from django.contrib import admin
from .models import TopicTag, SkillTag, UserProfile


class AdminTopicTag(admin.ModelAdmin):
    pass


class AdminSkillTag(admin.ModelAdmin):
    pass


class AdminUserProfile(admin.ModelAdmin):
    pass


admin.site.register(TopicTag, AdminTopicTag)
admin.site.register(SkillTag, AdminSkillTag)
admin.site.register(UserProfile, AdminUserProfile)
