from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase

class ArticleTestCases(TestCase):
    
    def setUp(self):
        token = Token.objects.get(user__username='test')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.force_authenticate(user=user)