from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Category, Food, Comment
from .serializers import CategorySerializer, FoodSerializer, CommentSerializer
from .permissions import MyIsAuthenticatedOrReadOnly, CommentAuthorPermission


class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodAPIView(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class CommentAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(food_id=self.kwargs.get('food_id'))

    def perform_create(self, serializer):
        food = get_object_or_404(Food, pk=self.kwargs.get('food_id'))
        serializer.validated_data['user'] = self.request.user
        serializer.validated_data['food'] = food
        serializer.save()
        return serializer


class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        MyIsAuthenticatedOrReadOnly,
        CommentAuthorPermission
    ]
    lookup_url_kwarg = 'comment_id'