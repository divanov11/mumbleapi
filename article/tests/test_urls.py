from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from article.views import *

class TestUrls(SimpleTestCase):
    
    def test_articles_url_is_resolved(self):
        url = reverse('articles')
        self.assertEquals(resolve(url).func,articles)

    def test_articles_created_url_is_resolved(self):
        url = reverse('create-article')
        self.assertEquals(resolve(url).func,createArticle)

    def test_articles_vote_url_is_resolved(self):
        url = reverse('vote')
        self.assertEquals(resolve(url).func,updateVote)