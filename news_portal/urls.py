
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include('protect.urls')),
   path('', include('new.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
]
