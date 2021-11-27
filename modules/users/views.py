from modules.places.serializers import CategorySerializer, DepartmentSerializer, SubCategorySerializer, TypePlaceSerializer
from django.http import response
from modules.places.models import Province, Department, TouristicPlace
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegisterAccountSerializer, AccountSerializer, FavouriteSerializer, FavouriteTpSerializer, \
    PreferenceCategorySerializer, PreferenceTypePlaceSerializer, PreferenceSubCategorySerializer, AccountSerializerAux, MessageSerializer
from .models import *
import jwt   
import datetime
from rest_framework import status
import requests
import time
import json
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# Create your views here.

class RegisterView(APIView):
    def post(self, request):

        typeplaces=request.data.pop('type_place')
        categories= request.data.pop('category')
        subcategories=request.data.pop('subcategory')

        email=request.data['email']
        serializer=AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        if(serializer.is_valid()):

            accounts= Account.objects.all()
            nserializer=RegisterAccountSerializer(accounts, many=True)
            for dicts in nserializer.data:
                if dicts['email']==email:
                    accountId=dicts['account_id']

            for tp in typeplaces:
                tpserializer=PreferenceTypePlaceSerializer(data={"type_place": tp, "user": accountId, "status":True})
                tpserializer.is_valid(raise_exception=True)
                tpserializer.save()
        
            for cat in categories:
                catserializer=PreferenceCategorySerializer(data={"category": cat, "user": accountId, "status":True})
                catserializer.is_valid(raise_exception=True)
                catserializer.save()        
        
            for subcat in subcategories:
                subcatserializer=PreferenceSubCategorySerializer(data={"subcategory": subcat, "user":accountId, "status":True})
                subcatserializer.is_valid(raise_exception=True)
                subcatserializer.save()      

        trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)
        return Response(serializer.data) 

class ListUsers(APIView): 
    def get(self, request):
        users=Account.objects.all()
        serializer=AccountSerializer(users,many=True)
        return Response(serializer.data)

class ListPreferedTypePlace(APIView): 

    def get(self, request):

        preferedTypePlaces= PreferenceTypePlace.objects.all()
        serializer=PreferenceTypePlaceSerializer(preferedTypePlaces, many=True)
        return Response(serializer.data)

class ChatbotPreferenceMessage(APIView):
    def post(self, request):

        #create the message, store it in db
        request.data['is_user']=True
        msgserializer = MessageSerializer(data=request.data)
        msgserializer.is_valid(raise_exception=True)
        msgserializer.save()
        
        #call the chatbot service
        if(msgserializer.is_valid()):

            url = "http://ec2-54-235-10-1.compute-1.amazonaws.com/prediction"
            payload = json.dumps({
                "msg": request.data['text'],
            })
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            botResponseMsg=response.json()['msg']

            #save chatbot message to db
            request.data['is_user']=False
            request.data['text']=botResponseMsg
            botmsgserializer= MessageSerializer(data=request.data)
            botmsgserializer.is_valid(raise_exception=True)
            botmsgserializer.save()

            #show chatbot and human message
            combinedResponse=Response()
            combinedResponse.data = {
            'human_message': msgserializer.data,
            'bot_response':  botmsgserializer.data
            }
            return combinedResponse
        else:
            response=Response()
            response.data = {
                'message': 'error'
            }
            return response

class ListPreferedCategory(APIView): 

    def get(self, request):

        preferedCategories= PreferenceCategory.objects.all()
        serializer=PreferenceCategorySerializer(preferedCategories, many=True)
        return Response(serializer.data)

class ListPreferedSubCategory(APIView): 

    def get(self, request):

        preferedSubCategories= PreferenceSubCategory.objects.all()
        serializer=PreferenceSubCategorySerializer(preferedSubCategories, many=True)
        return Response(serializer.data)

class AddCategoryPreference(APIView):
    def post(self, request):
        serializer = PreferenceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)

        return Response(serializer.data)

class AddTypePlacePreference(APIView):
    def post(self, request):
        serializer = PreferenceTypePlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)
        
        return Response(serializer.data)

class AddSubCategoryPreference(APIView):
    def post(self, request):
        serializer = PreferenceSubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
        requests.request("GET", trainingUrl)

        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']

        user = Account.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        #removed expiration field
        payload = {
            'id': user.account_id,
            'iat': datetime.datetime.utcnow()
        }

        print('payload', payload)

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        print('token', token)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id': user.account_id,
            'jwt': token
        }
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Account.objects.filter(account_id=payload['id']).first()
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class AddFavourites(APIView):
    def post(self, request):
        serializer = FavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 

class ListFavourites(APIView):
    def get(self,request):
        favourites = Favourite.objects.all()
        serializer=FavouriteSerializer(favourites, many=True)
        return Response(serializer.data)

class DeleteFavouriteByPlaceAndUser(APIView):
    def delete(self, request, user, tp):
       favourite=Favourite.objects.filter(touristic_place=tp).filter(user=user)
       if favourite:
           favourite.delete()
           return response.JsonResponse({'status':'ok'},status=status.HTTP_200_OK)
       return response.JsonResponse({'status':'error'},status=status.HTTP_400_BAD_REQUEST)

class ListPreferredTypePlacesByUser(APIView): 
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        preferredTypePlaces= PreferenceTypePlace.objects.filter(user=pk)
        tpserializer = PreferenceTypePlaceSerializer(preferredTypePlaces, many=True)
        tplist=[]
        for tp in tpserializer.data:
            if tp['type_place'] not in tplist:
                tplist.append(tp['type_place'])
        typeplaces=TypePlace.objects.filter(typeplace_id__in=tplist)

        typePlaceSerializer = TypePlaceSerializer(typeplaces,many=True)

        
        response = Response()

        response.data = {
            'typeplaces': typePlaceSerializer.data,
        }
        return response

class ListPreferredCategoriesByUser(APIView): 
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        preferredCategories= PreferenceCategory.objects.filter(user=pk)
        catserializer = PreferenceCategorySerializer(preferredCategories, many=True)

        catlist=[]
        for cat in catserializer.data:
            if cat['category'] not in catlist:
                catlist.append(cat['category'])
        categories=Category.objects.filter(category_id__in=catlist)

        categorySerializer = CategorySerializer(categories,many=True)

        
        response = Response()

        response.data = {
            'categories': categorySerializer.data,
        }
        return response


class ListPreferredSubCategoriesByUser(APIView): 
    def get(self, request, pk):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('Unauthenticated!')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated!')

        preferredSubCategories= PreferenceSubCategory.objects.filter(user=pk)
        subcatserializer = PreferenceSubCategorySerializer(preferredSubCategories, many=True)

        subcatlist=[]

        for subcat in subcatserializer.data:
            if subcat['subcategory'] not in subcatlist:
                subcatlist.append(subcat['subcategory'])

        subcategories=SubCategory.objects.filter(subcategory_id__in=subcatlist)
        subCategorySerializer = SubCategorySerializer(subcategories, many=True)
        
        response = Response()

        response.data = {
            'subcategories': subCategorySerializer.data,
        }

        return response

class ListFavouriteDepartment(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        favouritePlaces = Favourite.objects.filter(user=pk).values_list('touristic_place', flat=True)
        
        id_list = []
        
        for e in favouritePlaces:
            id_list.append(e)

        tp = TouristicPlace.objects.filter(touristicplace_id__in=id_list).values_list('province', flat=True)

        province_list = []

        for p in tp:
            province_list.append(p)

        provinces = Province.objects.filter(province_id__in=province_list).values_list('department', flat=True)

        department_list = []
        
        for d in provinces:
            department_list.append(d)

        print("DL: ", department_list)

        departments = Department.objects.filter(department_id__in=department_list)

        print("Depart: ", departments)

        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class ListFavourite(APIView):
    def get(self, request, pk, pk2):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        favouritePlaces = Favourite.objects.filter(user=pk, touristic_place__province__department=pk2)

        serializer = FavouriteTpSerializer(favouritePlaces, many=True)
        return Response(serializer.data)


class ListPreference(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        prcategory = PreferenceCategory.objects.filter(user=pk, status=True)
        catserializer = PreferenceCategorySerializer(prcategory, many=True)
        catlist=[]

        for cat in catserializer.data:
            catlist.append(cat['category'])
        
        categories=Category.objects.filter(category_id__in=catlist)
        categorySerializer = CategorySerializer(categories,many=True)

        ######

        prsubcategory = PreferenceSubCategory.objects.filter(user=pk, status=True)
        subcatserializer = PreferenceSubCategorySerializer(prsubcategory, many=True)
        subcatlist=[]

        for subcat in subcatserializer.data:
            subcatlist.append(subcat['subcategory'])

        subcategories=SubCategory.objects.filter(subcategory_id__in=subcatlist)
        subCategorySerializer = SubCategorySerializer(subcategories, many=True)

        ######

        prtypeplace = PreferenceTypePlace.objects.filter(user=pk, status=True)
        tpserializer = PreferenceTypePlaceSerializer(prtypeplace, many=True)
        tplist=[]

        for tp in tpserializer.data:
            tplist.append(tp['type_place'])

        typeplaces=TypePlace.objects.filter(typeplace_id__in=tplist)
        typePlaceSerializer = TypePlaceSerializer(typeplaces,many=True)

        
        response = Response()

        response.data = {
            'categories': categorySerializer.data,
            'typeplaces': typePlaceSerializer.data,
            'subcategories': subCategorySerializer.data,
        }
        return response

class ListTypePlacePreference(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        prtypeplace = PreferenceTypePlace.objects.filter(user=user_id)

        serializer = PreferenceTypePlaceSerializer(prtypeplace, many=True)
        return Response(serializer.data)


class UpdateCategoryPreference(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        cat = request.data['category']
        prtypeplace = PreferenceCategory.objects.filter(user=user_id, category=cat).first()
        serializer = PreferenceCategorySerializer(prtypeplace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
            requests.request("GET", trainingUrl)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTypePlacePreference(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user_id = request.data['user']
        tp = request.data['type_place']
        prtypeplace = PreferenceTypePlace.objects.filter(user=user_id, type_place=tp).first()
        serializer = PreferenceTypePlaceSerializer(prtypeplace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
            requests.request("GET", trainingUrl)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateSubcategoryPreference(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = request.data['user']
        subcat=request.data['subcategory']
        prsubcategory=PreferenceSubCategory.objects.filter(user=user_id, subcategory=subcat).first()
        serializer = PreferenceSubCategorySerializer(prsubcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trainingUrl="http://ec2-34-234-66-195.compute-1.amazonaws.com/trainmatrices"
            requests.request("GET", trainingUrl)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountListView(APIView):
    def get(self, request):

        accounts= Account.objects.all()
        serializer=RegisterAccountSerializer(accounts, many=True)
        return Response(serializer.data)

class UpdateUser(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = request.data['user']
        account = Account.objects.filter(account_id=user_id).first()


        if 'image' not in request.FILES:
            image = []
        else:
            image = dict(request.FILES)['image']
            image = image[0]

        serializer = AccountSerializerAux(account, data=request.data, context={'image': image})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateMessage(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UpdateMessage(APIView):
    def put(self, request):
        message_id = request.data['message_id']
        message = Message.objects.get(pk=message_id,)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageListView(APIView):
    def get(self, request):

        messages= Message.objects.all()
        serializer=MessageSerializer(messages, many=True)

        # now=datetime.datetime.now().strftime('%Y-%m-%d')
        # yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # for dict in serializer.data:
        #     if dict['date']==now:
        #         dict['date']='Today'
        #     elif dict['date']==yesterday:
        #         dict['date']='Yesterday'
        return Response(serializer.data)

class MessageById(APIView):
    def get(self, request, pk):
        messages=Message.objects.filter(pk=pk)
        serializer=MessageSerializer(messages,many=True)

        # now=datetime.datetime.now().strftime('%Y-%m-%d')
        # yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # for dict in serializer.data:
        #     if dict['date']==now:
        #         dict['date']='Today'
        #     elif dict['date']==yesterday:
        #         dict['date']='Yesterday'

        return Response(serializer.data)
    
    def delete(self,request,pk):
        message=Message.objects.filter(pk=pk)
        if message.exists():
            serializer=MessageSerializer(message)
            message.delete()
            return Response({"Success!":"Message deleted succesfully"})
        else:
            response = Response({"Error":"Message does not exist!"})
        return response


class MessageByUserId(APIView):
    def get(self, request, pk):
        messages=Message.objects.filter(user=pk)
        serializer=MessageSerializer(messages,many=True)

        # now=datetime.datetime.now().strftime('%Y-%m-%d')
        # yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # for dict in serializer.data:
        #     if dict['date']==now:
        #         dict['date']='Today'
        #     elif dict['date']==yesterday:
        #         dict['date']='Yesterday'

        return Response(serializer.data)

class SubCategoryPrefById(APIView):
    def get(self, request, pk):
        subcategorypref=PreferenceSubCategory.objects.filter(pk=pk)
        serializer=PreferenceSubCategorySerializer(subcategorypref, many=True)
        return Response(serializer.data)
    def delete(self,request,pk):
        subcategorypref = PreferenceSubCategory.objects.filter(pk=pk)
        if subcategorypref.exists():
            serializer=PreferenceSubCategorySerializer(subcategorypref)
            subcategorypref.delete()
            return Response({"Success!":"Subcategory Preference deleted successfully"})
        else:
            return Response({"Error": "Subcategory Preference does not exist!"})