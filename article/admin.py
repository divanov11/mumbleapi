from django.contrib import admin
from datetime import timedelta
from .models import Article, ArticleComment, ArticleVote


class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'user', 'get_utc',)
    search_fields = ('title',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


class AdminArticleComment(admin.ModelAdmin):
    list_display = ('article', 'user', 'get_utc',)
    search_fields = ('article',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


class AdminArticleVote(admin.ModelAdmin):
    list_display = ('article', 'user', 'value','get_utc') 
    search_fields = ('article',)
    list_filter = ('created', 'value',)
    empty_value_display = '-empty field-'

    def get_utc(self, obj):
        return obj.created + timedelta(minutes=330)

    get_utc.short_description = 'Created (UTC)'


admin.site.register(Article, AdminArticle)
admin.site.register(ArticleComment, AdminArticleComment)
admin.site.register(ArticleVote, AdminArticleVote)
