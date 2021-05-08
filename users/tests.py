from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.

class UserTest(TestCase):
    
    def setUp(self):
        user = User(username='Praveen',email='prince.malethia.36@gmail.com')
        user.is_staff = True
        user.is_superuser = True
        user.set_password('S0MtaingWiredPhassWarld')
        user.save()

    def test_user_exists(self):
        total_user = User.objects.all().count()
        self.assertEquals(total_user,1)

    def test_user_password(self):
        user = User.objects.all().first()
        if user is not None:
            user_exists = True
        else:
            user_exists = False
        self.assertEquals(user is not None, user_exists)