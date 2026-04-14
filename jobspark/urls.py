"""
jobspark/urls.py
================
Root URL configuration — delegates everything to the 'jobs' app.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # All application routes live in jobs/urls.py
    path('', include('jobs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
