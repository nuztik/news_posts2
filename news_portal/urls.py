
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),
   path('admin/', admin.site.urls),
   path('', include('protect.urls')),
   path('', include('new.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
]
