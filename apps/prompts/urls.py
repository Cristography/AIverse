"""
URL Configuration for Prompts app
"""

from django.urls import path
from . import views

app_name = 'prompts'

urlpatterns = [
    # Main prompt pages
    path('', views.PromptListView.as_view(), name='list'),
    path('prompt/<slug:slug>/', views.PromptDetailView.as_view(), name='detail'),
    path('submit/', views.PromptCreateView.as_view(), name='create'),
    
    # User-specific pages
    path('my-prompts/', views.MyPromptsView.as_view(), name='my_prompts'),
    path('my-bookmarks/', views.MyBookmarksView.as_view(), name='my_bookmarks'),
    
    # AJAX actions
    path('bookmark/<slug:slug>/', views.BookmarkToggleView.as_view(), name='bookmark_toggle'),
]