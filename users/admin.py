from django.contrib import admin
from .models import TopicTag, SkillTag, UserProfile


class AdminTopicTag(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty field-'


class AdminSkillTag(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty field-'


class AdminUserProfile(admin.ModelAdmin):
    search_fields = ('user',)
    list_filter = ('user', 'email_verified',)
    empty_value_display = '-empty field-'


admin.site.register(TopicTag, AdminTopicTag)
admin.site.register(SkillTag, AdminSkillTag)
admin.site.register(UserProfile, AdminUserProfile)
