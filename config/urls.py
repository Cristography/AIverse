"""
Main URL Configuration for the project
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.prompts.urls')),
    path('users/', include('apps.users.urls')),
    path('blog/', include('apps.blog.urls')),     
    path('news/', include('apps.news.urls')),     
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Customize admin site
admin.site.site_header = "Prompt Library Admin"
admin.site.site_title = "Prompt Library"
admin.site.index_title = "Welcome to Prompt Library Administration"
