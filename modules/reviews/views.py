import requests
from modules.places.serializers import TouristicPlaceSerializer
from modules.places.models import TouristicPlace
from rest_framework.views import APIView
from .serializers import ReviewSerializer, PictureReviewSerializer, SOSReviewSerializer, TotalReviewSerializer, TotalReviewSerializerUser, \
    ReviewSerializerSR
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import *

# Create your views here.
class CreateReview(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        review_id = serializer.data['review_id']

        if 'image' not in request.FILES:
            images = []
        else:
            images = dict(request.FILES.lists())['image']

        arr_img = []
        for img in images:
            data = img.file
            arr_img.append(data)

        number_images = len(arr_img)
        if len(arr_img) > 0:
            for n in range(0, number_images):
                aux = dict({"image": images[n], "number": n + 1, "review": review_id})
                serializer_picture = PictureReviewSerializer(data=aux)
                serializer_picture.is_valid(raise_exception=True)
                serializer_picture.save()
        trainingUrl="http://ec2-3-95-56-39.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)
        return Response(serializer.data)

class SOSCreateReview(APIView):
    def post(self, request):
        serializer=SOSReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        review_id = serializer.data['review_id']

        if 'image' not in request.FILES:
            images = []
        else:
            images = dict(request.FILES.lists())['image']

        arr_img = []
        for img in images:
            data = img.file
            arr_img.append(data)

        number_images = len(arr_img)
        if len(arr_img) > 0:
            for n in range(0, number_images):
                aux = dict({"image": images[n], "number": n + 1, "review": review_id})
                serializer_picture = PictureReviewSerializer(data=aux)
                serializer_picture.is_valid(raise_exception=True)
                serializer_picture.save()
        trainingUrl="http://ec2-3-95-56-39.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)
        return Response(serializer.data)


class ReviewTouristicPlaceListView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        reviews = Review.objects.filter(touristic_place=pk)

        serializer = TotalReviewSerializer(reviews, many=True)

        return Response(serializer.data)

class ReviewUserListView(APIView):
    def get(self,request,pk):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('Unauthenticated!')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated!')

        reviews = Review.objects.filter(user=pk)

        serializer = TotalReviewSerializerUser(reviews,many=True)

        return Response(serializer.data)

class AllReviewsForSR(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializerSR(reviews, many=True)
        return Response(serializer.data)
