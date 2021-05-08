from django.test import TestCase
from django.contrib.auth.models import User
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