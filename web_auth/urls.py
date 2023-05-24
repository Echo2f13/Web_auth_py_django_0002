from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include('events.urls')),
    path('admin/',admin.site.urls),
    path('user/',include('user.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]
