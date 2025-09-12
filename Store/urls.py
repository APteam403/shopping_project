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

urlpatterns = [
    path('search-test/', views.search_test_page, name='search_test'),
    path('autocomplete/', views.ProductAutocompleteView.as_view(), name='product-autocomplete'),
    path('', views.index_page, name='index_page'),
    path('weblog/', views.weblog, name='weblog_page'),
    path('about-us/', views.about_us, name='aboutus_page'),
    path('detail/<slug:slug>/', views.detail_page, name='detail_page'),
    path('category/<slug:slug>/', views.category_page, name='category_page'),
    path('views_hot/', views.views_hot_page, name='views_hot_page'),
    path('api/', include(router.urls)),
]