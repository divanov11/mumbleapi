from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import include, path, reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
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

    # The reason to remove the admin user create test is that we are not going to create any admin using API  
    # We might need to get this back so its commented


    # def test_admin_create_account(self):
    #     url = reverse('users-api:register')
    #     data = {
    #         'username': 'admin',
    #         'email': 'admin@gmail.com',
    #         'password': 'admin'
    #     } 
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(User.objects.count(), 2)
    #     self.assertEqual(User.objects.get(username='admin'),'admin')

    # def test_admin_login_account(self):
    #     user = User.objects.create(username='admin')
    #     user.set_password('admin')
    #     user.save()
    #     url = reverse('users-api:login')
    #     data = {
    #         'username': 'admin',
    #         'password': 'admin'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(User.objects.get().username, 'admin')


    def test_users_follow_url(self):
        client = APIClient()
        # authenticating the user
        client.force_authenticate(user=self.test_user)
        url = 'users-api:follow-user'
        # getting user which to follow
        user_following = self.another_user.userprofile
        # get following user count before follow
        user_followers_before = user_following.followers.count()
        response = client.post(url,args=['praveen'])
        user_followers_after = user_following.followers.count()

        # test if follow was successful

        # self.assertEqual(user_followers_after,user_followers_before+1)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)