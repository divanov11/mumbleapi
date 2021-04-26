from django.contrib import admin
from .admin import (Article,ArticleComment,ArticleVote)
# Register your models here.

admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(ArticleVote)