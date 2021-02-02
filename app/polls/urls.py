from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include("djoser.urls")),
    path('auth/', include("djoser.urls.authtoken")),
    path('admin/', admin.site.urls),
    path('', include("content.urls"))
]
