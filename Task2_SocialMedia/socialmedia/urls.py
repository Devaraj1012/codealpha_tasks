from django.contrib import admin
from django.urls import path, include  # ✅ You forgot to import include
from django.conf import settings        # ✅ Needed for media settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),     # ✅ Make sure this comes after include is imported
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
