"""
Custom context processors to make data available in all templates
"""

from django.conf import settings


def site_settings(request):
    """
    Add site-wide settings to template context
    """
    return {
        'SITE_NAME': 'Prompt Library',
        'SITE_DESCRIPTION': 'Discover and share AI prompts',
        'AVAILABLE_LANGUAGES': settings.LANGUAGES,
        'CURRENT_LANGUAGE': request.session.get('language', 'en'),
        'CURRENT_THEME': request.session.get('theme', 'light'),
    }