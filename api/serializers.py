from rest_framework import serializers

from .models import Food, Category, Comment


class FoodSerializerForCategory(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'text', 'price', 'discount', 'created']


class CategorySerializer(serializers.ModelSerializer):
    # foods = serializers.StringRelatedField(many=True)
    # foods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # foods = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                             view_name='food-detail')
    # foods = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    # url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    foods = FoodSerializerForCategory(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'foods']

    def create(self, validated_data):
        foods = validated_data.pop('foods')
        category = Category.objects.create(**validated_data)

        foods_list = []
        for food in foods:
            foods_list.append(
                Food(category=category, **food)
            )

        Food.objects.bulk_create(foods_list)
        return category


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'text', 'price', 'discount', 'created', 'category']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user']
        read_only_fields = ['user']