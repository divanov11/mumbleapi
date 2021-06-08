import re
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.

from ..models import SkillTag, TopicTag

from users.views import email_validator

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

        # Creating another account to test following 

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
        client = APIClient()
        # authenticating the user
        client.force_authenticate(user=self.test_user)
        # get following user count before follow
        user_followers_before = self.another_user.userprofile.followers.count()
        response = client.post('/api/users/praveen/follow/',args=[self.another_user.username])
        user_followers_after = self.another_user.userprofile.followers.count()

        # test if follow was successful

        self.assertEqual(user_followers_after,user_followers_before+1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_login(self):
        url = 'users-api:login'
        reversed_url = reverse(url)
        data = {
            'username':'praveen',
            'password':'SomethingRandomPassword@123'
        }
        client = APIClient()
        response = client.post(reversed_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = json.loads(response.content.decode('UTF-8'))
        # if response[0]:
        #     print("Login Token Being Generated Correctly")
        # if response[1]:
        #     print("Rrefresh Token also genrerate Correctly")
        # if response.content.get("username") == data.get('username'):
        #     print("Correct User fetched")


    def test_user_profile_update_view(self):
        url = 'users-api:profile_update'
        reversed_url = reverse(url)
        data = {
            'username':'TEST'
        }
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.patch(reversed_url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_user_email_is_valid(self):
        email = 'rshalem@gmail.com'
        self.assertEqual(email_validator(email), 'rshalem@gmail.com')
        print('PASSED EMAIL VERIFICATION TEST')

    def test_user_following_view(self):
        url = 'users-api:following'
        reversed_url = reverse(url)
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_mumbles_view(self):
        url = 'users-api:user-mumbles'
        reversed_url = reverse(url,args=[self.test_user.username])
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_articles_view(self):
        url = 'users-api:user-articles'
        reversed_url = reverse(url,args=[self.test_user.username])
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_password_change_view(self):
        url = 'users-api:password-change'
        reversed_url = reverse(url)
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        data = {
            'new_password':"Test@123",
            'new_password_confirm':"Test@123"
        }
        response = client.post(reversed_url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_send_activate_email_view(self):
        url = 'users-api:send-activation-email'
        reversed_url = reverse(url)
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.post(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_skills(self):
        url = 'users-api:update_skills'
        reversed_url = reverse(url)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.patch(reversed_url, [
            {'name': 'javascript'}
        ])
        response_json = json.loads(response.content)
        tag = SkillTag.objects.get(name='javascript')
        self.assertEqual(tag.name, 'javascript')
        self.assertEqual(response_json['skills'], [{'name': 'javascript'}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_interests(self):
        url = 'users-api:update_interests'
        reversed_url = reverse(url)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.patch(reversed_url, [
            {'name': 'agile'}
        ])
        response_json = json.loads(response.content)
        tag = TopicTag.objects.get(name='agile')
        self.assertEqual(tag.name, 'agile')
        self.assertEqual(response_json['interests'], [{'name': 'agile'}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_follow_view(self):
        # test_user should be following 0 people at the start
        user_following_before = self.test_user.following.count()
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post('/api/users/praveen/follow/',args=[self.another_user.username])

        # check the following endpoint to verify that test_user comes back
        url = 'users-api:following'
        reversed_url = reverse(url)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reversed_url)
        user_following_after = self.test_user.following.count()
        self.assertEqual(user_following_after,user_following_before + 1)

