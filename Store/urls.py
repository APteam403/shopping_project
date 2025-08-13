from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('brands', views.BrandViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('concerns', views.ConcernViewSet)
router.register('skintypes', views.SkinTypeViewSet)
router.register('ingredients', views.IngredientViewSet)

urlpatterns = router.urls + [
    path('search-test/', views.search_test_page, name='search_test'),
    path('autocomplete/', views.ProductAutocompleteView.as_view(), name='product-autocomplete'),
]