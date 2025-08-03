from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class SkinType(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Concerns(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Integration(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    skin_type = models.ManyToManyField(SkinType)
    concerns_targeted = models.ManyToManyField(Concerns)
    integrations = models.ManyToManyField(Integration)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0 )
    image_urls = models.URLField(unique=True)
    tags = models.CharField(max_length=255)

