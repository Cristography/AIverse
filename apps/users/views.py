from django.shortcuts import render

# Create your views here.
"""
Class-Based Views for Users app
"""

from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import UserProfile


class UserRegisterView(CreateView):
    """
    User registration view
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """
    User login view
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """
    User logout view
    """
    template_name = 'users/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Display user profile
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        # Get user's recent prompts
        context['recent_prompts'] = user.prompts.filter(is_published=True).order_by('-created_at')[:6]
        
        # Get stats
        context['total_prompts'] = user.prompts.filter(is_published=True).count()
        context['total_bookmarks'] = user.bookmarks.count()
        context['total_views'] = sum(p.views for p in user.prompts.filter(is_published=True))
        
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)