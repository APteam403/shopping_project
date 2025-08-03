from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('brands', views.BrandViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('concerns', views.ConcernViewSet)
router.register('skinTypes', views.SkinTypeViewSet)
router.register('integrations', views.IntegrationViewSet)

urlpatterns = router.urls