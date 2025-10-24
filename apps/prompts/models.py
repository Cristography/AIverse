"""
Models for the Prompts app
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Categories to organize prompts (e.g., Writing, Coding, Marketing)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Prompt(models.Model):
    """
    Main Prompt model - stores AI prompts submitted by users
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    MODEL_CHOICES = [
        ('chatgpt', 'ChatGPT'),
        ('claude', 'Claude'),
        ('gemini', 'Gemini'),
        ('midjourney', 'Midjourney'),
        ('stable-diffusion', 'Stable Diffusion'),
        ('other', 'Other'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(help_text="Brief description of what this prompt does")
    prompt_text = models.TextField(help_text="The actual prompt to be copied")
    
    # Classification
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='prompts')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    ai_model = models.CharField(max_length=50, choices=MODEL_CHOICES, default='chatgpt')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    # Author and engagement
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')
    views = models.PositiveIntegerField(default=0)
    upvotes = models.PositiveIntegerField(default=0)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Prompt.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('prompts:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def __str__(self):
        return self.title


class Bookmark(models.Model):
    """
    Users can bookmark prompts to save them for later
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'prompt')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.prompt.title}"