from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.register_view, name='contact_page'),
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
]