from django.test import RequestFactory,TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
# Create your tests here.

class AccountTests(APITestCase):
    def test_create_account(self):
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