"""
Forms for Blog app
"""

from django import forms
from .models import BlogPost, BlogComment


class BlogPostForm(forms.ModelForm):
    """
    Form for creating/editing blog posts
    """
    publish_now = forms.BooleanField(
        required=False,
        initial=False,
        label='Publish immediately',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = BlogPost
        fields = ['title', 'excerpt', 'content', 'featured_image', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog post title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of your post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your blog post content here...'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'comma, separated, tags'
            }),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            return ', '.join(tag_list)
        return tags


class BlogCommentForm(forms.ModelForm):
    """
    Form for adding comments to blog posts
    """
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'content': 'Your Comment'
        }