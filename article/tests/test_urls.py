from django.test import SimpleTestCase
from django.urls import reverse , resolve
from article.views import *

class TestUrls(SimpleTestCase):
    
    def test_articles_url_is_resolved(self):
        url = reverse('mumbles-api-articles:articles')
        self.assertEquals(resolve(url).func,articles)

    def test_articles_created_url_is_resolved(self):
        url = reverse('mumbles-api-articles:create-article')
        self.assertEquals(resolve(url).func,createArticle)

    def test_articles_vote_url_is_resolved(self):
        url = reverse('mumbles-api-articles:article-vote')
        self.assertEquals(resolve(url).func,updateVote)

    def test_get_article_url_is_resolved(self):
        url = reverse('mumbles-api-articles:get-article',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,getArticle)

    def test_edit_article_url_is_resolved(self):
        url = reverse('mumbles-api-articles:edit-article',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,editArticle)

    def test_delete_article_url_is_resolved(self):
        url = reverse('mumbles-api-articles:delete-article',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,deleteArticle)

    def test_edit_article_comment_url_is_resolved(self):
        url = reverse('mumbles-api-articles:edit-article-comment',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,editArticleComment)

    def test_delete_article_comment_url_is_resolved(self):
        url = reverse('mumbles-api-articles:delete-article-comment',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,deleteArticleComment)