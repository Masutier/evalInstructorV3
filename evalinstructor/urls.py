from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', include('administracion.urls')),
    path('', include('loadlists.urls')),
    path('', include('evaluaciones.urls')),

    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('validarHash', validarHash, name='validarHash'),
    path('about', about, name='about'),
    path('recuperacion', recuperacion, name='recuperacion'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 401 Unauthorized
# 403 Forbidden
# 404 Not Found
