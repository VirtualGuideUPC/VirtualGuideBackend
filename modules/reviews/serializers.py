import cloudinary.uploader
from rest_framework import serializers
from .models import *
from modules.users.models import Account



class PictureReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureReview
        fields = ['image', 'number', "review"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        res = cloudinary.uploader.upload(instance.image)
        instance.image = res['secure_url']
        instance.url = res['secure_url']
        instance.save()
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField('get_user_name')
    icon=serializers.SerializerMethodField('get_icon')
    images = PictureReviewSerializer(many=True)  

    class Meta:
        model = Review
        fields = ['review_id', 'comment', 'comment_ranking', 'date', 'ranking', 'touristic_place', 'user_name', 'icon','images']
    
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_user_name(self, obj):
        return obj.user.name

    def get_icon(self, obj):
        return obj.user.icon


class SOSReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields = ['review_id','comment','comment_ranking','date','ranking','touristic_place','user']
    
    def create(self,validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class ReviewTpSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Review
        fields = ['review_id', 'user_name', 'date', 'comment', 'ranking'] 

    def get_user_name(self, obj):
        return obj.user.name

class PictureReviewTpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureReview
        fields = ['url', 'number']


class TotalReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    user_picture=serializers.SerializerMethodField('get_user_picture')
    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Review
        fields = ['review_id', 'user_name','user_picture', 'date', 'comment', 'ranking','images']

    def get_images(self,obj):
        if PictureReview.objects.filter(review=obj.review_id).exists():
            qs = PictureReview.objects.filter(review=obj.review_id)
            serializer = PictureReviewTpSerializer(instance=qs, many=True)
            return serializer.data
        else:
            return []

    def get_user_name(self, obj):
        return obj.user.name

    def get_user_picture(self,obj):
        return obj.user.icon

class TotalReviewSerializerUser(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    user_name = serializers.SerializerMethodField('get_user_name')
    user_id=serializers.SerializerMethodField('get_account_id')
    touristic_place_name = serializers.SerializerMethodField('get_touristic_place_name')
    touristic_place_id=serializers.SerializerMethodField('get_touristic_place_id')
    province = serializers.SerializerMethodField('get_province')

    class Meta:
        model = Review
        fields = ['review_id','user_id', 'user_name', 'date', 'comment', 'ranking', 'images','touristic_place_id','touristic_place_name', 'province']

    def get_images(self,obj):
        if PictureReview.objects.filter(review=obj.review_id).exists():
            qs = PictureReview.objects.filter(review=obj.review_id)
            serializer = PictureReviewTpSerializer(instance=qs, many=True)
            return serializer.data
        else:
            return []

    def get_user_name(self, obj):
        return obj.user.name

    def get_account_id(self,obj):
        return obj.user.account_id

    def get_touristic_place_name(self,obj):
        return obj.touristic_place.name

    def get_province(self,obj):
        return obj.touristic_place.province.name

    def get_touristic_place_id(self,obj):
        return obj.touristic_place.touristicplace_id



class ReviewSerializerSR(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['ranking', 'touristic_place', 'user']

