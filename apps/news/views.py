"""
Class-Based Views for News app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import NewsArticle, NewsCategory


class NewsListView(ListView):
    """
    Display list of news articles
    """
    model = NewsArticle
    template_name = 'news/news_list.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = NewsArticle.objects.filter(is_published=True).select_related('category')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(subtitle__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by priority
        priority = self.request.GET.get('priority', '')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        
        # Breaking news (top priority)
        context['breaking_news'] = NewsArticle.objects.filter(
            is_published=True,
            priority='breaking'
        ).order_by('-published_at')[:3]
        
        # Featured articles
        context['featured_articles'] = NewsArticle.objects.filter(
            is_published=True,
            is_featured=True
        ).order_by('-published_at')[:4]
        
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_priority'] = self.request.GET.get('priority', '')
        
        return context


class NewsDetailView(DetailView):
    """
    Display single news article
    """
    model = NewsArticle
    template_name = 'news/news_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True).select_related('category')
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Related articles (same category)
        context['related_articles'] = NewsArticle.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id).order_by('-published_at')[:4]
        
        # Latest news
        context['latest_news'] = NewsArticle.objects.filter(
            is_published=True
        ).order_by('-published_at')[:5]
        
        return context


class CategoryNewsView(ListView):
    """
    Display news articles by category
    """
    model = NewsArticle
    template_name = 'news/category_news.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return NewsArticle.objects.filter(
            category__slug=category_slug,
            is_published=True
        ).select_related('category').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['category'] = NewsCategory.objects.get(slug=category_slug)
        context['categories'] = NewsCategory.objects.all()
        return context