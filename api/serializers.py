from django.db.models import Model
from rest_framework import serializers

from .models import Food, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)


class FoodSerializer(serializers.ModelSerializer):
    category_write = serializers.ChoiceField(
        choices=Category.objects.all(),
        write_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'text', 'price', 'discount', 'created', 'category', 'category_write']
        depth = 1
        # exclude = ['name']
        # read_only_fields = ['name']

    def create(self, validated_data):
        category_write = validated_data.pop("category_write")
        food = Food.objects.create(category=category_write, **validated_data)
        food.save()
        return food

    def update(self, instance, validated_data):
        instance.category = validated_data.pop("category_write") or instance.category
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

