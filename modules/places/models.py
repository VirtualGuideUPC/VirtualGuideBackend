from django.db import models
from django.db.models import Avg, OuterRef, Subquery

# Create your models here.

class TypePlace(models.Model):
    typeplace_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=255)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255, default='None')

class SubCategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=False, blank=False, default=1, on_delete=models.CASCADE)

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=255, default="")

class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, null=False, blank=False, default=1, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255, default="")

class TouristicPlace(models.Model):
    touristicplace_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cost_info = models.CharField(max_length=255)
    price = models.FloatField()
    schedule_info = models.CharField(max_length=255)
    historic_info = models.CharField(max_length=255)
    long_info = models.TextField()
    short_info = models.CharField(max_length=255)
    activities_info = models.CharField(max_length=255)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    tp_range = models.IntegerField()
    avg_ranking = models.FloatField(default=0.0)
    number_comments = models.IntegerField(default=0)
    province = models.ForeignKey(Province, null=False, blank=False, default=1, on_delete=models.CASCADE)
    type_place = models.ForeignKey(TypePlace, null=False, blank=False, default=1, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    isFavourite = models.BooleanField(default=False)

class FunFact(models.Model):
    funfact_id = models.AutoField(primary_key=True)
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default=1, on_delete=models.CASCADE, related_name="funfacts")
    fact = models.CharField(max_length=255, default="")

class PictureTouristicPlace(models.Model):
    ptouristicplace_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    number = models.IntegerField()
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default=1, on_delete=models.CASCADE, related_name="pictures")

class TouristicPlaceCategory(models.Model):
    tp_category_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=False, blank=False, default=1, on_delete=models.CASCADE)
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default=1, on_delete=models.CASCADE, related_name="categories")

