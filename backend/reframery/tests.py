from django.test import TestCase

# Create your tests here.
from reframery.models import CustomUser

class UserTestCase(TestCase):
    def setUp(self):
        user = CustomUser(email = "test@test.com")
        user.set_password("abc")
        user.first_name = "Jeff"
        user.last_name = "Bob"
        user.save()
        
    def test_user_created(self):
        user = CustomUser.objects.get(email="test@test.com")
        print(user)