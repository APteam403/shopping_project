from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class SkinTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinType
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'

class ConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concerns
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    product_id = serializers.UUIDField(read_only=True)
    rating = serializers.FloatField(read_only=True)

    brand = serializers.SlugRelatedField(slug_field='name', queryset=Brand.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    skin_type = serializers.SlugRelatedField(many=True, slug_field='name', queryset=SkinType.objects.all())
    concerns_targeted = serializers.SlugRelatedField(many=True,slug_field='name', queryset=Concerns.objects.all())
    ingredients = serializers.SlugRelatedField( many=True, slug_field='name', queryset=Ingredients.objects.all())
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tags.objects.all())
    