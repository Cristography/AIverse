"""
Django Admin configuration for News app
"""

from django.contrib import admin
from .models import NewsCategory, NewsArticle


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_editable = ['color']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'is_featured', 'is_published', 'views', 'published_at']
    list_filter = ['priority', 'is_published', 'is_featured', 'category', 'published_at']
    search_fields = ['title', 'subtitle', 'summary', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['priority', 'is_featured', 'is_published']
    readonly_fields = ['views', 'published_at', 'updated_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'source')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'tags')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Stats & Timestamps', {
            'fields': ('views', 'published_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )