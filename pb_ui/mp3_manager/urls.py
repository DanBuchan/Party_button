from django.urls import path
from . import views

app_name = "mp3_manager"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), 
    path("upload/", views.UploadView.as_view(), name="upload"), 
    path("delete/", views.DeleteView.as_view(), name="delete"), 
]
