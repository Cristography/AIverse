"""
URL Configuration for Blog app
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list and detail
    path('', views.BlogListView.as_view(), name='list'),
    path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    
    # Create post
    path('create/', views.BlogCreateView.as_view(), name='create'),
    
    # My posts
    path('my-posts/', views.MyBlogPostsView.as_view(), name='my_posts'),
    
    # Comments
    path('post/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
]