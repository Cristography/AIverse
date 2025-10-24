"""
Django Admin configuration for Prompts app
"""

from django.contrib import admin
from .models import Category, Prompt, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'ai_model', 'views', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'difficulty', 'ai_model', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'prompt_text', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'prompt_text')
        }),
        ('Classification', {
            'fields': ('category', 'difficulty', 'ai_model', 'tags')
        }),
        ('Author & Stats', {
            'fields': ('author', 'views', 'upvotes')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'prompt', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'prompt__title']
    readonly_fields = ['created_at']