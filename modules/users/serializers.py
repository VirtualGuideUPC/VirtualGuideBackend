from rest_framework.validators import UniqueTogetherValidator
from modules.places.models import Department
from modules.places.serializers import NearbyPlaceSerializer
from rest_framework import serializers
from .models import *
import cloudinary.uploader


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'name', 'last_name', 'birthday', 'country']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['touristic_place', 'user']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class FavouriteTpSerializer(serializers.ModelSerializer):
    touristic_place_detail = serializers.SerializerMethodField('get_tp')

    class Meta:
        model = Favourite
        fields = [ 'user', 'touristic_place_detail']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_tp(self, obj):
        tp = obj.touristic_place.touristicplace_id
        tplace = TouristicPlace.objects.filter(touristicplace_id=tp).first()
        serializer = NearbyPlaceSerializer(tplace)
        return serializer.data

class PreferenceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceCategory
        fields = ['category', 'user', 'status']
        validators = [
            UniqueTogetherValidator(
                queryset=PreferenceCategory.objects.all(),
                fields=('category','user')
            )
        ]
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.user = validated_data.get('user', instance.user)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class PreferenceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceSubCategory
        fields = ['subcategory','user','status']
        validators = [
            UniqueTogetherValidator(
                queryset=PreferenceSubCategory.objects.all(),
                fields=('subcategory','user')
            )
        ]
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.subcategory=validated_data.get('subcategory', instance.subcategory)
        instance.user=validated_data.get('user', instance.user)
        instance.status=validated_data.get('status', instance.status)
        instance.save()
        return instance

class PreferenceTypePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceTypePlace
        fields = ['type_place', 'user', 'status']
        validators = [
            UniqueTogetherValidator(
                queryset=PreferenceTypePlace.objects.all(),
                fields=('type_place','user')
            )
        ]
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type_place = validated_data.get('type_place', instance.type_place)
        instance.user = validated_data.get('user', instance.user)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'email', 'password', 'name', 'last_name', 'birthday', 'country']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AccountSerializerAux(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'name', 'last_name', 'birthday', 'country', 'icon']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        if len(self.context.get("image")) == 0:
            instance.icon = validated_data.get('icon', instance.icon)
        else:
            image = self.context.get("image")
            res = cloudinary.uploader.upload(image)
            instance.icon = validated_data.get('icon', res['secure_url'])
        instance.save()
        return instance
