from django.contrib import admin
from django.urls import include, path

from polls.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("admin/", admin.site.urls),
    path("", include("content.urls")),
]
urlpatterns += swagger_urls
