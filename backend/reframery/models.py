from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
import jwt
import datetime
from django.conf import settings

def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(20, chars)
    
# Create your models here.
class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

class Community(models.Model):
    name = models.CharField(max_length=255)
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), db_index=True, unique=True)
    USERNAME_FIELD = 'email'
    phone_number = models.CharField(max_length=255, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
    admin = models.BooleanField(null=True)
    register_time = models.DateTimeField(auto_now = True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    user_image = models.URLField(null=True) #S3 storage for url
    validate_code = models.CharField(max_length=255, default = generate_activation_key(""))
    validate_status = models.BooleanField(default=False)
    validate_time = models.DateTimeField(null=True)
    REQUIRED_FIELDS = []
    
    
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Item(models.Model):
    class Category(models.TextChoices):
        PRODUCT = "product", _("Product")
        SERVICE = "service", _("Service")
        EXPERTISE = "expertise", _("Expertise")
    
    category = models.CharField(choices = Category.choices, max_length=9)
    name = models.CharField(max_length=255)
    image = models.URLField() #S3 Storage for url
    price = models.DecimalField(decimal_places = 2, max_digits = 10)
    stock = models.IntegerField()
    description = models.TextField()
    discount = models.DecimalField(decimal_places = 2, max_digits = 10)
    subcategory_id = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Feedback(models.Model):
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    rating = models.IntegerField()
    created_time = models.DateTimeField(auto_now = True)
    description = models.TextField()

class Transaction(models.Model):
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'sender_id')
    receiver_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'receiver_id')
    time = models.DateTimeField(auto_now = True)
    amount = models.IntegerField()
    txid = models.CharField(max_length=255)

class Order(models.Model):
    buyer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'buyer_id')
    seller_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'seller_id') 
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)

"""
:description: Wallet information. Has a one to one relationship customUser.
"""
class Wallet(models.Model):
    customUser = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    address = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)