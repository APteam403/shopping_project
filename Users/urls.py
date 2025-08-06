from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.contact_page, name='contact_page'),
    path('sign-in', views.signin_page, name='signin_page')
]