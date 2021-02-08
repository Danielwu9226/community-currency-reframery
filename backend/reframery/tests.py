from django.test import TestCase
import unittest

# Create your tests here.
from reframery.models import CustomUser, SubCategory

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
    
    #other user fields should be possible too based on the .get() param.
    def test_get_first_name(self):
        user = CustomUser.objects.get(email="test@test.com")
        return user.first_name == "Jeff"

class SubCategoryTestCase(TestCase):
    def setUp(self):
        user = CustomUser(email = "test@test.com")
        user.set_password("abc")
        user.first_name = "Jeff"
        user.last_name = "Bob"
        user.save()

        subcategory_name = "test"
        subcategory = SubCategory(name = subcategory_name, user_id = user)
        subcategory.save()

    def test_subcategory_created(self):
        user = CustomUser.objects.get(email = "test@test.com")
        subcategory = SubCategory.objects.get(user_id = user.id)
        return subcategory is not None
    
    @unittest.expectedFailure
    def test_subcategory_not_possible_no_user_id(self):
        SubCategory.objects.get(user_id = 1000000)

