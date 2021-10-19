from django.db import models
from django.contrib.auth.models import AbstractUser
from modules.places.models import TypePlace, TouristicPlace, Category, SubCategory
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)

class Account(AbstractUser):
    account_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    user_picture= models.CharField(max_length=255, default="")
    email = models.CharField(max_length=70, unique=True, default="")
    password = models.CharField(max_length=255)
    token_notification = models.CharField(max_length=70, default="")
    country = models.ForeignKey(Country, null=False, blank=False, default=1, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    birthday = models.DateField(default="2021-08-17")
    icon = models.CharField(max_length=255, default='None')
    is_foreign = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(Account,null=False,blank=False, default=1, on_delete=models.CASCADE)
    is_user=models.BooleanField(default=False)
    date = models.DateField(default="2021-08-16")
    time = models.TimeField(auto_now_add=True)
    url = models.CharField(max_length=300, default=None, blank=True, null=True)

class Favourite(models.Model):
    favourite_id = models.AutoField(primary_key=True)
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, null=False, blank=False, default=1, on_delete=models.CASCADE)    

class PreferenceCategory(models.Model):
    preference_category_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=False, blank=False, default=1, on_delete=models.CASCADE)    
    user = models.ForeignKey(Account, null=False, blank=False, default=1, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

class PreferenceTypePlace(models.Model):
    preference_typeplace_id = models.AutoField(primary_key=True)
    type_place = models.ForeignKey(TypePlace, null=False, blank=False, default=1, on_delete=models.CASCADE)    
    user = models.ForeignKey(Account, null=False, blank=False, default=1, on_delete=models.CASCADE)   
    status = models.BooleanField(default=False)

class PreferenceSubCategory(models.Model):
    preference_subcategory_id = models.AutoField(primary_key=True)
    subcategory = models.ForeignKey(SubCategory, null=False, blank=False, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, null=False, blank=False, default=1, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)