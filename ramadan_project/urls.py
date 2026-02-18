from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('timetable.urls')),
    path('', include('timetable.frontend_urls')),
]

if settings.DEBUG:
  static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
  if static_dirs:
    urlpatterns += static(settings.STATIC_URL, document_root=static_dirs[0])
  elif getattr(settings, 'STATIC_ROOT', None):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
