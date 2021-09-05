from django.urls import path
from .views import CreateReview, ReviewTouristicPlaceListView, ReviewUserListView

urlpatterns = [
    path('reviews/create/', CreateReview.as_view()),
    path('reviews/tp/<str:pk>/', ReviewTouristicPlaceListView.as_view()),
    path('reviews/user/<str:pk>/', ReviewUserListView.as_view()),
]
