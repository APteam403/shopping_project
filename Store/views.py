from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('tags', 'skin_type', 'integrations', 'concerns_targeted').all()
    serializer_class = ProductSerializer

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        brand = self.get_object()
        products = Product.objects.filter(brand=brand)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

class ConcernViewSet(ModelViewSet):
    queryset = Concerns.objects.all()
    serializer_class = ConcernSerializer

class SkinTypeViewSet(ModelViewSet):
    queryset = SkinType.objects.all()
    serializer_class = SkinTypeSerializer

class IntegrationViewSet(ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
