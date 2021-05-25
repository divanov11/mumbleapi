from django.contrib import admin
from .models import Article, ArticleComment, ArticleVote


class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'user', 'created',)
    search_fields = ('title',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'


class AdminArticleComment(admin.ModelAdmin):
    list_display = ('article', 'user', 'created',)
    search_fields = ('article',)
    list_filter = ('created',)
    empty_value_display = '-empty field-'


class AdminArticleVote(admin.ModelAdmin):
    list_display = ('article', 'user', 'value',) 
    search_fields = ('article',)
    list_filter = ('created', 'value',)
    empty_value_display = '-empty field-'


admin.site.register(Article, AdminArticle)
admin.site.register(ArticleComment, AdminArticleComment)
admin.site.register(ArticleVote, AdminArticleVote)
