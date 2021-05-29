from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase , APIClient
import json
# Create your tests here.

class FeedTestsViews(APITestCase):

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
        url = 'mumbles-api:mumble-create'
        reversed_url = reverse(url)
        data = {
            'content':"Mumble Test Post"
        }
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.post(reversed_url, data)
        self.mumble = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_users_url(self):
        url = 'mumbles-api:mumbles'
        reversed_url = reverse(url)
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        response = client.get(reversed_url)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('count'),1)

    def test_mumbles_edit_view(self):
        url = 'mumbles-api:mumble-edit'
        reversed_url = reverse(url,args=[self.mumble.get('id')])
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        data = {
            'content':"Mumble Post edited"
        }
        response = client.patch(reversed_url,data, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('content'),data.get('content'))
        self.mumble = response_data

    def test_mumbles_details_view(self):
        client = APIClient()
        client.force_authenticate(user=self.test_user)
        url = 'mumbles-api:mumble-details'
        reversed_url = reverse(url,args=[self.mumble.get('id')])
        response = client.get(reversed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
