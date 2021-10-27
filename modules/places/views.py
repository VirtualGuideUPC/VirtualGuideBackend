from .services import PlaceService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CategoryTpSerializer, CategorySerializer, SubCategorySerializer, TypePlaceSerializer, NearbyPlaceSerializer, TouristicPlaceCategorySerializer, TouristicPlaceSerializer, PictureTouristicPlaceSerializer, FunFactSerializer
from .models import *
from modules.reviews.models import Review
from modules.reviews.serializers import ReviewTpSerializer, TotalReviewSerializer
from django.db.models import Avg
import jwt

# Create your views here

class CreateTouristicPlace(APIView):
    def post(self, request):
        serializer = TouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AddTpCategory(APIView):
    def post(self, request):
        serializer = TouristicPlaceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TypePlaceListView(APIView):
    def get(self, request):

        typePlaces= TypePlace.objects.all()
        serializer=TypePlaceSerializer(typePlaces, many=True)
        return Response(serializer.data)

class CategoryListView(APIView):
    def get(self, request):

        categories= Category.objects.all()
        serializer=CategorySerializer(categories, many=True)
        return Response(serializer.data)

class SubCategoryListView(APIView):
    def get(self, request):
        subCategories= SubCategory.objects.all()
        serializer=SubCategorySerializer(subCategories, many=True)
        return Response(serializer.data)

class TouristicPlaceListView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlaces = TouristicPlace.objects.all()
        serializer = TouristicPlaceSerializer(touristicPlaces, many=True)
        return Response(serializer.data)

class TouristicPlaceById(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlace = TouristicPlace.objects.filter(touristicplace_id=pk).first()
        serializer = TPSerializer(touristicPlace)
        
        tppictures = PictureTouristicPlace.objects.filter(touristic_place=pk)
        picturesSerializer = PictureTouristicPlaceSerializer(tppictures, many=True)

        categorystp =  TouristicPlaceCategory.objects.filter(touristic_place=pk)
        categorystpSerializer = CategoryTpSerializer(categorystp, many=True)

        
        reviews = Review.objects.filter(touristic_place=pk)

        review_count = Review.objects.filter(touristic_place=pk).count()
        
        review_avg = Review.objects.filter(touristic_place=pk).aggregate(Avg('ranking'))
        
        funFacts= FunFact.objects.filter(touristic_place=pk)

        fin_avg = review_avg.get('ranking__avg')

        print('review_avg: ', review_avg)

        #reviewsSerializer = ReviewTpSerializer(reviews, many=True)
        reviewsSerializer = TotalReviewSerializer(reviews, many=True)

        funFactsSerializer= FunFactSerializer(funFacts, many=True)

        response = Response()

        simExp1 = TouristicPlace.objects.filter(type_place=touristicPlace.type_place).exclude(touristicplace_id=pk)
        categories = TouristicPlaceCategory.objects.filter(touristic_place=pk).values_list('category', flat=True)

        cat_list = []
        
        for c in categories:
            cat_list.append(c)
        
        
        cTp = TouristicPlaceCategory.objects.filter(category__in=cat_list).values_list('touristic_place', flat=True)
        
        setps = []
        
        for t in cTp:
            setps.append(t)


        simExp2 = TouristicPlace.objects.filter(touristicplace_id__in=setps).exclude(touristicplace_id=pk)

        simExpFinal = simExp1 | simExp2

        simExpSer = NearbyPlaceSerializer(simExpFinal, many=True)

        print(type(funFactsSerializer.data))

        funfactstr=[]
        for funfact in funFactsSerializer.data:
            funfactstr.append(funfact['fact'])

        print((funFactsSerializer.data))

        response.data = {
            'id': touristicPlace.touristicplace_id,
            'pictures': picturesSerializer.data,
            'name': touristicPlace.name,
            'short_info':touristicPlace.short_info,
            'long_info': touristicPlace.long_info,
            'categories': categorystpSerializer.data,
            'latitude': touristicPlace.latitude,
            'longitude': touristicPlace.longitude,
            'province':touristicPlace.province.name,
            'avg_ranking': fin_avg,
            'number_comments': review_count,
            'schedule_info':touristicPlace.schedule_info,
            'fun_facts':funfactstr,
            'reviews': reviewsSerializer.data,
            'similarExperiences': simExpSer.data,
            'isFavourite': touristicPlace.isFavourite
        }
        return response


class CreatePictureTouristicPlace(APIView):
   def post(self, request):
        serializer = PictureTouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CreateFunFact(APIView):
    def post(self, request):
        serializer= FunFactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ListAllFunFacts(APIView):
    def get(self,request):
        funFacts= FunFact.objects.all()
        serializer=FunFactSerializer(funFacts, many=True)
        return Response(serializer.data)

class FunFactByTouristicPlaceId(APIView):
    def get(self,request, pk):
        funFacts=FunFact.objects.filter(touristic_place=pk)
        serializer = FunFactSerializer(funFacts, many=True)
        return Response(serializer.data)

class PictureTouristicPlaceListView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        pictureTouristicPlaces = PictureTouristicPlace.objects.filter(touristic_place=pk)
        serializer = PictureTouristicPlaceSerializer(pictureTouristicPlaces, many=True)
        return Response(serializer.data)

class NearbyPlaces(APIView):
    def post(self, request):
        touristicPlaces = TouristicPlace.objects.all()
        
        lat = request.data['latitude']
        lon = request.data['longitude']

        placeService = PlaceService(lat, lon) 
        
        tplist = placeService.tpnearbylist(touristicPlaces)
        
        serializer = NearbyPlaceSerializer(tplist, many=True)
        userId=request.data['user_id']

        url="http://ec2-3-95-56-39.compute-1.amazonaws.com/simusrec"
        payload = json.dumps({
            "user_id": userId
        })
        headers = {
            'Content-Type': 'application/json'
        }
       
        response = requests.request("GET", url, headers=headers, data=payload)
        
        try:
            recommendations=response.json()['recommendations']
        except:
            recommendations=[]

        # recommendations.append(75)

        for place in serializer.data:           
            if place['touristicplace_id'] in recommendations:
              place.update({"isRecommended":True})
            else:
              place.update({"isRecommended":False})

        return Response(serializer.data)