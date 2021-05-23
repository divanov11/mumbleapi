import re
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
import json

from users.views import email_validator

# This test will start with 2 users.  
# One user (test_user) will follow another user (another_user)
# We verify that the test_users' following count increases by one, and also verify another_user's
# followers count increases by one at the end of this test case
class FollowingAnotherUserTests(APITestCase):
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

        data = {
            'username':'praveen',
            'email':'praveen@gmail.com',
            'password':'SomethingRandomPassword@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='praveen').username,data.get('username'))
        self.another_user = User.objects.get(username='praveen')


    def test_users_follow_view(self):
        # test user should be following 0 people at the start
        user_following_before = self.test_user.following.count()
        # another_user should have 0 followers at the start
        user_followers_before = self.another_user.userprofile.followers.count()

        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.post('/api/users/praveen/follow/',args=[self.another_user.username])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = 'users-api:following'
        reversed_url = reverse(url)
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.get(reversed_url)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_following_after = self.test_user.following.count()
        user_followers_after = self.another_user.userprofile.followers.count()

        self.assertEqual(user_followers_after,user_followers_before + 1)
        self.assertEqual(user_following_after,user_following_before + 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        