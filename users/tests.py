from django.test import RequestFactory,TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import include, path, reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from . import views
# Create your tests here.

class AccountTests(APITestCase):

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

    def test_list_accounts(self):
        url = reverse('users-api:users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resolve(url).func,views.users)

    def test_list_recommended_accounts(self):
        url = reverse('users-api:users-recommended')
        user = User.objects.get(username='test')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resolve(url).func,views.usersRecommended)