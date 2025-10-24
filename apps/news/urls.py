"""
URL Configuration for News app
"""

from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # News list and detail
    path('', views.NewsListView.as_view(), name='list'),
    path('article/<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
    
    # Category-specific news
    path('category/<slug:slug>/', views.CategoryNewsView.as_view(), name='category'),
]