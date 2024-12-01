from django.conf import settings
from django.urls import path
from home import views as home_view
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view.download_audio, name='download_audio'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])