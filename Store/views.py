from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializrer
