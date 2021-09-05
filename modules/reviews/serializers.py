import cloudinary.uploader
from rest_framework import serializers
from .models import *
from modules.users.models import Account

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['review_id', 'comment', 'comment_ranking', 'date', 'ranking', 'touristic_place', 'user']
    
    
    def create(self, validated_data):
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

class PictureReviewTpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureReview
        fields = ['url', 'number']


class TotalReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Review
        fields = ['review_id', 'user_name', 'date', 'comment', 'ranking', 'images']

    def get_images(self,obj):
        if PictureReview.objects.filter(review=obj.review_id).exists():
            qs = PictureReview.objects.filter(review=obj.review_id)
            serializer = PictureReviewTpSerializer(instance=qs, many=True)
            return serializer.data
        else:
            return []

    def get_user_name(self, obj):
        return obj.user.name

