from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from uuid import uuid4
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = 'Brand'
        
    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255) 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
class SkinType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = 'Skin type'

    def __str__(self):
        return self.name
class Concerns(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = 'Concern'

    def __str__(self):
        return self.name
class Ingredients(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        verbose_name = 'Ingredient'

    def __str__(self):
        return self.name
class Tags(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    views_count = models.PositiveIntegerField(default=0)

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    skin_type = models.ManyToManyField(SkinType)
    concerns_targeted = models.ManyToManyField(Concerns)
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tags, related_name='products')

    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.FloatField( validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0 )
    slug = models.SlugField(unique=True, blank=True, max_length=255) 
    is_active = models.BooleanField(default=True)
    image_urls = models.URLField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
