from django.contrib.auth.models import User
from django.urls import include, path, reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
from users.views import followUser
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
        self.test_user = User.objects.get(username='test')
        self.test_user_pwd = 'test@123'

    def test_users_follow_url(self):
        url = 'users-api:follow-user'
        reversed_url = reverse(url,args=['praveen'])
        self.assertEqual(resolve(reversed_url).func,followUser)