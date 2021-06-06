from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
from article.views import create_article

class ArticleTestCases(APITestCase):

    def setUp(self):
        url = reverse('users-api:register')
        data = {
            'username':'test',
            'email':'test@gmail.com', 
            'password':'test@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_create_article(self):
        url = reverse('mumbles-api-articles:create-article')
        user = User.objects.get(username='test')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            'title':"Title of Article",
            'content':"Content for article",
            'tags':"Tags for article"
        }
        response = client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resolve(url).func,create_article)