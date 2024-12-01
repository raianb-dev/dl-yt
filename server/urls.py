from django.conf import settings
from django.urls import path
from home import views as home_view
from django.conf.urls.static import static


urlpatterns = [
        path('', home_view.redirect_to_home, name='in'),
    path('convertt-mp3/youtube/', home_view.download_audio, name='download_audio'),
    path('<path:undefined_path>', home_view.redirect_to_home, name='404'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
