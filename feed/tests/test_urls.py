from django.urls import reverse , resolve
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from feed import views
# Create your tests here.

class FeedTestsUrls(APITestCase):

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

    def test_mumbles_url(self):
        url = 'mumbles-api:mumbles'
        reversed_url = reverse(url)
        self.assertEqual(resolve(reversed_url).func,views.mumbles)
    
    def test_mumbles_create_url(self):
        url = 'mumbles-api:mumble-create'
        reversed_url = reverse(url)
        self.assertEqual(resolve(reversed_url).func,views.create_mumble)
    
    def test_mumbles_edit_url(self):
        url = 'mumbles-api:mumble-edit'
        reversed_url = reverse(url,args=['9812-3ehj9-238d39-8hd23h'])
        self.assertEqual(resolve(reversed_url).func,views.edit_mumble)
    
    def test_mumbles_detail_url(self):
        url = 'mumbles-api:mumble-details'
        reversed_url = reverse(url,args=['9812-3ehj9-238d39-8hd23h'])
        self.assertEqual(resolve(reversed_url).func,views.mumble_details)
    
    def test_mumbles_remumble_url(self):
        url = 'mumbles-api:mumble-remumble'
        reversed_url = reverse(url)
        self.assertEqual(resolve(reversed_url).func,views.remumble)

    def test_mumbles_vote_url(self):
        url = 'mumbles-api:posts-vote'
        reversed_url = reverse(url)
        self.assertEqual(resolve(reversed_url).func,views.update_vote)

    def test_mumbles_delete_url(self):
        url = 'mumbles-api:delete-mumble'
        reversed_url = reverse(url,args=['9812-3ehj9-238d39-8hd23h'])
        self.assertEqual(resolve(reversed_url).func,views.delete_mumble)

    def test_mumbles_comments_url(self):
        url = 'mumbles-api:mumble-comments'
        reversed_url = reverse(url,args=['9812-3ehj9-238d39-8hd23h'])
        self.assertEqual(resolve(reversed_url).func,views.mumble_comments)
