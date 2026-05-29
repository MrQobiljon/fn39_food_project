from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Category, Food


class CategoryAPIView(APIView):
    def get(self, request: Request, pk: int = None):
        if not pk:
            categories = Category.objects.all()
            category_list = []
            for category in categories:
                category_list.append(
                    {
                        'id': category.pk,
                        'name': category.name
                    }
                )
            return Response(category_list)
        else:
            category = Category.objects.get(pk=pk)
            return Response(model_to_dict(category))


class FoodAPIView(APIView):
    pass