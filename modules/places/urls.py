from django.urls import path
from .views import AddTpCategory, TouristicPlaceById, TouristicPlaceListView, CreateTouristicPlace, PictureTouristicPlaceListView, CreatePictureTouristicPlace, NearbyPlaces, ListAllFunFacts, FunFactByTouristicPlaceId, CreateFunFact, TouristicPlaceWithFavourite

urlpatterns = [
    path('places/create/', CreateTouristicPlace.as_view()),
    path('places/list/', TouristicPlaceListView.as_view()),
    path('places/tp/<str:pk>/', TouristicPlaceById.as_view()),
    path('places/tp/<str:pk1>/<str:pk2>/',TouristicPlaceWithFavourite.as_view()),
    path('places/createphotos/', CreatePictureTouristicPlace.as_view()),
    path('places/<str:pk>/photos/', PictureTouristicPlaceListView.as_view()),
    path('places/addCategory/', AddTpCategory.as_view()),
    path('places/nearby/', NearbyPlaces.as_view()),
    path('places/funfacts/',ListAllFunFacts.as_view()),
    path('places/funfacts/<str:pk>/',FunFactByTouristicPlaceId.as_view()),
    path('places/funfact/',CreateFunFact.as_view())
]   