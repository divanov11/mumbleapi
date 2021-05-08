from django.test import RequestFactory,TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
# Create your tests here.

class UserTest(TestCase):
    
    def setUp(self):
        user = User(username='Praveen',email='prince.malethia.36@gmail.com')
        user.is_staff = True
        user.is_superuser = True
        self.user_password = 'S0MtaingWiredPhassWarld'
        user.set_password(self.user_password)
        user.save()
        self.user = user

    def test_user_exists(self):
        total_user = User.objects.all().count()
        self.assertEquals(total_user,1)

    def test_user_password(self):
        self.assertTrue(self.user.check_password(self.user_password))

class UsersTestAPI(APITestCase):

    def test_login_via_api(self):
        token = Token.objects.get(user__username='test')
        client = APIClient()
        client.login(username='test', password='test@123')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.login()