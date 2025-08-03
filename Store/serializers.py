from rest_framework import serializers
from .models import *

class ProductSerializrer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    product_id = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    skin_type = serializers.PrimaryKeyRelatedField(many=True, queryset=SkinType.objects.all())
    concerns_targeted = serializers.PrimaryKeyRelatedField(many=True, queryset=Concerns.objects.all())
    integrations = serializers.PrimaryKeyRelatedField(many=True, queryset=Integration.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tags.objects.all())