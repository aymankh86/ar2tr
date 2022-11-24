from django.urls import path
from .views import index, search, suggest

urlpatterns = [
    path('', index, name='index'),
    path('search', search, name='search'),
    path('suggest', suggest, name='suggest'),
]