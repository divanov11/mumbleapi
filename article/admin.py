from django.contrib import admin
from .models import Article, ArticleComment, ArticleVote


class AdminArticle(admin.ModelAdmin):
    pass


class AdminArticleComment(admin.ModelAdmin):
    pass


class AdminArticleVote(admin.ModelAdmin):
    pass


admin.site.register(Article, AdminArticle)
admin.site.register(ArticleComment, AdminArticleComment)
admin.site.register(ArticleVote, AdminArticleVote)
