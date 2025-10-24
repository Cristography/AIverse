"""
Models for News app
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class NewsCategory(models.Model):
    """
    Categories for news articles
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    color = models.CharField(max_length=20, default='primary', help_text="Bootstrap color class")
    
    class Meta:
        verbose_name_plural = "News Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """
    News article model
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('breaking', 'Breaking News'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    subtitle = models.CharField(max_length=200, blank=True, help_text="Optional subtitle")
    
    # Content
    summary = models.TextField(max_length=300, help_text="Brief summary for list view")
    content = models.TextField(help_text="Full article content")
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, help_text="News source/author")
    
    # Classification
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='articles')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    tags = models.CharField(max_length=200, blank=True)
    
    # Engagement
    views = models.PositiveIntegerField(default=0)
    
    # Status
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    
    # Timestamps
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_published', '-published_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def __str__(self):
        return self.title