from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'rating']
    list_filter = ['brand', 'category', 'skin_type' ,'tags', 'concerns_targeted']
    search_fields = ['name', 'brand__name', 'category__name']
    filter_horizontal =['skin_type', 'tags', 'concerns_targeted', 'ingredients']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(SkinType)
class SkinTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(Concerns)
class ConcernsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']
