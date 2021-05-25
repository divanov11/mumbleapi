from django.contrib import admin
from datetime import timedelta
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
    list_display = ('username','get_utc','email_verified')
    search_fields = ('user',)
    list_filter = ('user', 'email_verified',)
    empty_value_display = '-empty field-'

    def get_utc(self, obj):
        return obj.user.date_joined + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


admin.site.register(TopicTag, AdminTopicTag)
admin.site.register(SkillTag, AdminSkillTag)
admin.site.register(UserProfile, AdminUserProfile)
