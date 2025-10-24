"""
Class-Based Views for Blog app
"""

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

from .models import BlogPost, BlogCategory, BlogComment
from .forms import BlogPostForm, BlogCommentForm


class BlogListView(ListView):
    """
    Display list of published blog posts
    """
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').select_related('author', 'category')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['featured_posts'] = BlogPost.objects.filter(
            status='published', 
            is_featured=True
        )[:3]
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class BlogDetailView(DetailView):
    """
    Display single blog post with comments
    """
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('author', 'category')
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get approved comments
        context['comments'] = self.object.comments.filter(is_approved=True).select_related('author')
        context['comments_count'] = context['comments'].count()
        
        # Comment form
        context['comment_form'] = BlogCommentForm()
        
        # Related posts
        context['related_posts'] = BlogPost.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:3]
        
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Create new blog post (only for logged-in users)
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:my_posts')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Auto-publish if checkbox is checked
        if form.cleaned_data.get('publish_now'):
            form.instance.status = 'published'
            form.instance.published_at = timezone.now()
        
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """
    Display blog posts by logged-in user
    """
    model = BlogPost
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by('-created_at')


class AddCommentView(LoginRequiredMixin, CreateView):
    """
    Add comment to blog post
    """
    model = BlogComment
    form_class = BlogCommentForm
    
    def form_valid(self, form):
        post = BlogPost.objects.get(slug=self.kwargs['slug'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'slug': self.kwargs['slug']})