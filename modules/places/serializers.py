from rest_framework import serializers
from .models import *

class TouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlace
        fields = ['name', 'cost_info', 'price', 'schedule_info', 'historic_info', 'long_info', 'short_info', 'activities_info', 'latitude', 'longitude', 'tp_range', 'province', 'type_place', 'isFavourite'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class TPSerializer(serializers.ModelSerializer):
    province_name = serializers.SerializerMethodField('get_province_name')
    picture = serializers.SerializerMethodField('get_picture')
    class Meta:
        model = TouristicPlace
        fields = ['touristicplace_id', 'name', 'short_info', 'latitude', 'longitude', 'picture','tp_range', 'province_name', 'avg_ranking', 'number_comments', 'isFavourite'] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_province_name(self, obj):
        pname = obj.province.name
        return pname
    
    def get_picture(self, obj):
        tp_id = obj.touristicplace_id
        tppicture = PictureTouristicPlace.objects.filter(touristic_place=tp_id).values_list('url', flat=True).first()
        return str(tppicture)  

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'name', 'photo']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class TypePlaceSerializer(serializers.ModelSerializer): 

    status=serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return False

    class Meta: 
        model = TypePlace
        fields =['typeplace_id','name','icon','status']
    
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PictureTouristicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureTouristicPlace
        fields = ['url', 'number', "touristic_place"] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PictureTpUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureTouristicPlace
        fields = ['url'] 

class TouristicPlaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristicPlaceCategory
        fields = ['category', "touristic_place"] 
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class CategoryTpSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    
    class Meta:
        model = TouristicPlaceCategory
        fields = ['category', 'name'] 

    def get_name(self, obj):
        return obj.category.name

class CategorySerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return False

    class Meta: 
        model = Category
        fields =['category_id', 'name', 'icon','status']

    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class SubCategorySerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()

    @staticmethod
    def get_status(obj):
        return False

    class Meta: 
        model = SubCategory
        fields =['subcategory_id', 'name', 'icon','status']

    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class NearbyPlaceSerializer(serializers.ModelSerializer):

    province_name = serializers.SerializerMethodField('get_province_name')
    picture = serializers.SerializerMethodField('get_picture')

    class Meta:
        model = TouristicPlace
        fields = ['touristicplace_id', 'name', 'short_info', 'latitude', 'longitude', 'picture','tp_range', 'province_name', 'avg_ranking', 'number_comments', 'isFavourite'] 

    def get_province_name(self, obj):
        pname = obj.province.name
        return pname
    
    def get_picture(self, obj):
        tp_id = obj.touristicplace_id
        tppicture = PictureTouristicPlace.objects.filter(touristic_place=tp_id).values_list('url', flat=True).first()
        return str(tppicture)  
    
 