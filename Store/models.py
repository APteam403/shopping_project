from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class SkinType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class Concerns(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class Integration(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    skin_type = models.ManyToManyField(SkinType)
    concerns_targeted = models.ManyToManyField(Concerns)
    integrations = models.ManyToManyField(Integration)
    tags = models.ManyToManyField(Tags, related_name='products')

    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0 )
    slug = models.SlugField(unique=True, blank=True, max_length=255) 
    image_urls = models.URLField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
