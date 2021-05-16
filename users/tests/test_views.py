from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
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


    def test_users_follow_url(self):
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