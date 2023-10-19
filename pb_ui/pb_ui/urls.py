from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("mp3_manager.urls", namespace="mp3_manager")),
    path("admin/", admin.site.urls),
]
