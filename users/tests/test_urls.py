# from django.conf.urls import url
# from django.urls import reverse , resolve
# from rest_framework import status
# from rest_framework.test import APITestCase
# from users.views import (
#     followUser , users , UserProfileUpdate , 
#     ProfilePictureUpdate , usersRecommended ,
#     user , userMumbles, userArticles, passwordChange,
#     sendActivationEmail, sendActivationEmail , activate)
# # Create your tests here.

# class AccountTests(APITestCase):

#     def setUp(self):
#         pass

#     def test_users_url(self):
#         url = 'users-api:users'
#         reversed_url = reverse(url)
#         response = self.client.get('/api/users/')
#         self.assertEqual(resolve(reversed_url).func,users)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_users_follow_url(self):
#         url = 'users-api:follow-user'
#         reversed_url = reverse(url,args=['praveen'])
#         self.assertEqual(resolve(reversed_url).func,followUser)

#     def test_user_profile_update_url(self):
#         url = 'users-api:profile_update'
#         reversed_url = reverse(url)
#         self.assertEqual(resolve(reversed_url).func.view_class,UserProfileUpdate)

#     def test_profile_update_photo_url(self):
#         url = 'users-api:profile_update_photo'
#         reversed_url = reverse(url)
#         resolved = resolve(reversed_url).func
#         self.assertEqual(resolved.view_class,ProfilePictureUpdate)

#     def test_users_recommended_url(self):
#         url = 'users-api:users-recommended'
#         reversed_url = reverse(url)
#         self.assertEqual(resolve(reversed_url).func,usersRecommended)

#     def test_user_url(self):
#         url = 'users-api:user'
#         reversed_url = reverse(url,args=['test'])
#         self.assertEqual(resolve(reversed_url).func,user)

#     def test_user_mumbles(self):
#         url = 'users-api:user-mumbles'
#         reversed_url = reverse(url,args=['test'])
#         self.assertEqual(resolve(reversed_url).func,userMumbles)

#     def test_user_articles_url(self):
#         url = 'users-api:user-articles'
#         reversed_url = reverse(url,args=['test'])
#         self.assertEqual(resolve(reversed_url).func,userArticles)

#     def test_user_password_url(self):
#         url = 'users-api:password-change'
#         reversed_url = reverse(url)
#         self.assertEqual(resolve(reversed_url).func,passwordChange)

#     def test_send_activation_email_url(self):
#         url = 'users-api:send-activation-email'
#         reversed_url = reverse(url)
#         self.assertEqual(resolve(reversed_url).func,sendActivationEmail)

#     def test_active_user_account_url(self):
#         url = 'users-api:verify'
#         reversed_url = reverse(url,args=['903u924u934u598348943','*&6g83chruhrweriuj'])
#         self.assertEqual(resolve(reversed_url).func,activate)