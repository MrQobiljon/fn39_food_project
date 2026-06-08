from django.db.models import Model
from rest_framework import serializers

from .models import Food, Category, Comment


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'text', 'price', 'discount', 'created', 'category']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user']
        read_only_fields = ['user']