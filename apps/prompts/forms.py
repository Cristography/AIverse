"""
Forms for Prompts app
"""

from django import forms
from .models import Prompt, Category


class PromptForm(forms.ModelForm):
    """
    Form for users to submit new prompts
    """
    
    class Meta:
        model = Prompt
        fields = ['title', 'description', 'prompt_text', 'category', 'difficulty', 'ai_model', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a catchy title for your prompt'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Briefly describe what this prompt does'
            }),
            'prompt_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Paste your full prompt here'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ai_model': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter comma-separated tags (e.g., creative, marketing, SEO)'
            }),
        }
        labels = {
            'title': 'Prompt Title',
            'description': 'Short Description',
            'prompt_text': 'Full Prompt',
            'category': 'Category',
            'difficulty': 'Difficulty Level',
            'ai_model': 'AI Model',
            'tags': 'Tags',
        }
    
    def clean_tags(self):
        """Clean and format tags"""
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Split by comma, strip whitespace, and rejoin
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            return ', '.join(tag_list)
        return tags