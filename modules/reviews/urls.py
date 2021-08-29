from django.urls import path
from .views import CreateReview, ReviewTouristicPlaceListView

urlpatterns = [
    path('reviews/create/', CreateReview.as_view()),
    path('reviews/tp/<str:pk>/', ReviewTouristicPlaceListView.as_view())
]   