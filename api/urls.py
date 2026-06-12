from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import (CategoryAPIViewSet, FoodApiViewSet, CommentAPIView)

router = DefaultRouter()
router.register('categories', CategoryAPIViewSet, basename='category')
router.register('foods', FoodApiViewSet)


urlpatterns = [
    path(
        'foods/<int:food_id>/comments/',
        CommentAPIView.as_view({'get': 'list', 'post': 'create'}),
        name='comment-list'),

    path(
        'foods/<int:food_id>/comments/<int:comment_id>/',
        CommentAPIView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='comment-detail'),

    path('', include(router.urls)),
]