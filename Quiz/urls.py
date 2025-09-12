from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.create_book, name='book_page'),
    path("analyze-skin/", views.analyze_skin_view, name="analyze_skin"),
    path('generate-routine/', views.generate_and_save_routine_view, name='generate_routine'),
]