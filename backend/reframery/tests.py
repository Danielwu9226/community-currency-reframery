from django.test import TestCase
import unittest

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
        return user is not None and type(user) == CustomUser
    
    @unittest.expectedFailure
    #should fail due to integrity error by the database.
    def test_duplicate_user_not_possible(self):
        CustomUser.objects.create(email = "test@test.com")
    
