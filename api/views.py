from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from unicodedata import category

from .models import Category, Food
from .serializers import CategorySerializer, FoodSerializer


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