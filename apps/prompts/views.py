"""
Class-Based Views for Prompts app
"""

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from .models import Prompt, Category, Bookmark
from .forms import PromptForm


class PromptListView(ListView):
    """
    Display list of all prompts with search and filter
    Anyone can view (no login required)
    """
    model = Prompt
    template_name = 'prompts/prompt_list.html'
    context_object_name = 'prompts'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Prompt.objects.filter(is_published=True).select_related('author', 'category')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty', '')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by AI model
        ai_model = self.request.GET.get('model', '')
        if ai_model:
            queryset = queryset.filter(ai_model=ai_model)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['-created_at', '-views', '-upvotes']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['selected_model'] = self.request.GET.get('model', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        
        # Get featured prompts for homepage
        context['featured_prompts'] = Prompt.objects.filter(is_featured=True, is_published=True)[:3]
        
        return context


class PromptDetailView(DetailView):
    """
    Display single prompt with full details
    Increments view count on each visit
    """
    model = Prompt
    template_name = 'prompts/prompt_detail.html'
    context_object_name = 'prompt'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Prompt.objects.filter(is_published=True).select_related('author', 'category')
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count (can be optimized with F() to avoid race conditions)
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user has bookmarked this prompt
        if self.request.user.is_authenticated:
            context['is_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user,
                prompt=self.object
            ).exists()
        else:
            context['is_bookmarked'] = False
        
        # Get related prompts (same category)
        context['related_prompts'] = Prompt.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:4]
        
        return context


class PromptCreateView(LoginRequiredMixin, CreateView):
    """
    Allow logged-in users to submit new prompts
    """
    model = Prompt
    form_class = PromptForm
    template_name = 'prompts/prompt_form.html'
    success_url = reverse_lazy('prompts:my_prompts')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your prompt has been submitted successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class MyPromptsView(LoginRequiredMixin, ListView):
    """
    Display prompts submitted by the logged-in user
    """
    model = Prompt
    template_name = 'prompts/my_prompts.html'
    context_object_name = 'prompts'
    paginate_by = 12
    
    def get_queryset(self):
        return Prompt.objects.filter(author=self.request.user).order_by('-created_at')


class MyBookmarksView(LoginRequiredMixin, ListView):
    """
    Display prompts bookmarked by the logged-in user
    """
    model = Bookmark
    template_name = 'prompts/my_bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 12
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('prompt', 'prompt__author')


class BookmarkToggleView(LoginRequiredMixin, View):
    """
    AJAX view to toggle bookmark status
    """
    def post(self, request, slug):
        prompt = get_object_or_404(Prompt, slug=slug, is_published=True)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, prompt=prompt)
        
        if not created:
            # Bookmark already exists, so remove it
            bookmark.delete()
            is_bookmarked = False
            message = 'Bookmark removed'
        else:
            is_bookmarked = True
            message = 'Bookmark added'
        
        # Return JSON response for AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_bookmarked': is_bookmarked,
                'message': message
            })
        
        # Fallback for non-AJAX requests
        messages.success(request, message)
        return redirect('prompts:detail', slug=slug)