from django.urls import path
from .views import CreateReview, ReviewTouristicPlaceListView, ReviewUserListView, AllReviewsForSR, SOSCreateReview

urlpatterns = [
    path('reviews/create/', SOSCreateReview.as_view()),
    path('reviews/tp/<str:pk>/', ReviewTouristicPlaceListView.as_view()),
    path('reviews/user/<str:pk>/', ReviewUserListView.as_view()),
    path('reviews/all', AllReviewsForSR.as_view()),

]
