from django.contrib.auth.models import User
from django.urls import path
from ..places.views import TypePlaceListView, CategoryListView, SubCategoryListView
from .views import AccountListView, ListPreferedSubCategory, ListPreferredTypePlacesByUser, ListPreferredSubCategoriesByUser, \
    ListPreferredCategoriesByUser, ListPreferedCategory, ListPreferedTypePlace, AddFavourite, AddCategoryPreference, \
    AddTypePlacePreference, ListFavourite, ListFavouriteDepartment, ListPreference, RegisterView, LoginView, \
    UpdateCategoryPreference, UpdateTypePlacePreference, UserView, LogoutView, UpdateUser, CreateMessage, MessageListView, \
    UpdateMessage, MessageById, MessageByUserId, UpdateSubcategoryPreference, AddSubCategoryPreference, SubCategoryPrefById

urlpatterns = [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/user/', UserView.as_view()),
    path('users/user/update/', UpdateUser.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/favourite/create/', AddFavourite.as_view()),
    path('users/preference/category/create/', AddCategoryPreference.as_view()),
    path('users/preference/typeplace/create/', AddTypePlacePreference.as_view()),
    path('users/preference/subcategory/create/', AddSubCategoryPreference.as_view()),
    path('users/prefrence/subcategory/<str:pk>', SubCategoryPrefById.as_view()),
    path('users/<str:pk>/favourites/departments/', ListFavouriteDepartment.as_view()),
    path('users/<str:pk>/favourites/departments/<str:pk2>/', ListFavourite.as_view()),
    path('users/preferences/<str:pk>/', ListPreference.as_view()),
    path('users/getCategories/<str:pk>/', ListPreferredCategoriesByUser.as_view()),
    path('users/getSubCategories/<str:pk>/', ListPreferredSubCategoriesByUser.as_view()),
    path('users/getTypePlaces/<str:pk>/', ListPreferredTypePlacesByUser.as_view()),    
    path('users/preference/category/update/', UpdateCategoryPreference.as_view()),
    path('users/preference/subcategory/update/', UpdateSubcategoryPreference.as_view()),
    path('users/preference/typeplace/update/', UpdateTypePlacePreference.as_view()),
    path('users/getAllTypePlaces/',TypePlaceListView.as_view()),
    path('users/getAllSubcategories/', SubCategoryListView.as_view()),
    path('users/getAllCategories/', CategoryListView.as_view()),
    path('users/getAllPreferenceTypePlaces/',ListPreferedTypePlace.as_view()),
    path('users/getAllPreferenceCategories/',ListPreferedCategory.as_view()),
    path('users/getAllPreferenceSubCategories/',ListPreferedSubCategory.as_view()),
    path('users/getAllUsers/',AccountListView.as_view()),
    path('users/message/create/', CreateMessage.as_view()),
    path('users/message/update/', UpdateMessage.as_view()),
    path('users/getAllMessages/', MessageListView.as_view()),
    path('users/message/id/<str:pk>',MessageById.as_view()),
    path('users/message/userid/<str:pk>', MessageByUserId.as_view())
]