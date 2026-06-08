from django.urls import path

from .views import (CategoryAPIView, CategoryRetrieveAPIView,
                    FoodAPIView, FoodRetrieveAPIView,
                    CommentAPIView, CommentRetrieveAPIView)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view()),

    path('foods/', FoodAPIView.as_view()),
    path('foods/<int:pk>/', FoodRetrieveAPIView.as_view()),

    path('foods/<int:food_id>/comments/', CommentAPIView.as_view()),
    path('foods/<int:food_id>/comments/<int:comment_id>/', CommentRetrieveAPIView.as_view()),
]