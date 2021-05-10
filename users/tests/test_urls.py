from django.contrib.auth.models import User
from django.urls import include, path, reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
from users.views import followUser
# Create your tests here.

class AccountTests(APITestCase):

    def setUp(self):
        pass

    def test_users_follow_url(self):
        url = 'users-api:follow-user'
        reversed_url = reverse(url,args=['praveen'])
        self.assertEqual(resolve(reversed_url).func,followUser)