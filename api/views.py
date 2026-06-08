from django.db.models import Model
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .models import Category, Food, Comment
from .serializers import CategorySerializer, FoodSerializer, CommentSerializer
from .permissions import MyIsAuthenticatedOrReadOnly, CommentAuthorPermission


class CategoryAPIView(APIView):
    def get(self, request: Request, pk: int = None):
        if not pk:
            categories = Category.objects.all()
            return Response(CategorySerializer(categories, many=True).data)
        else:
            category = get_object_or_404(Category, pk=pk)
            return Response(CategorySerializer(category).data)

    def post(self, request: Request, pk = None):

        if pk:
            return Response({"message": "Method POST not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(**serializer.validated_data)
        return Response(CategorySerializer(category).data)

    def put(self, request: Request, pk: int = None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            category.name = serializer.validated_data.get("name", category.name)
            category.save()

            return Response(CategorySerializer(category).data)
        else:
            return Response({"message": "Method PUT not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request: Request, pk: int = None):
        if not pk:
            return Response({"message": "Method DELETE not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            category = get_object_or_404(Category, pk=pk)
            category.delete()
            return Response({"message": "Category deleted successful"}, status=status.HTTP_204_NO_CONTENT)


class FoodAPIView(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly]


    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return self.serializer_class
        return self.serializer_class


class FoodRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'food_id'
    permission_classes = [MyIsAuthenticatedOrReadOnly]

    def get_object(self):
        return super().get_object()


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