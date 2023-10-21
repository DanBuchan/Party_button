from django.urls import path
from . import views

app_name = "mp3_manager"
urlpatterns = [
    path("delete/<int:pk>/", views.DeleteView.as_view(), name='delete_track'), 
    path("solo/<int:pk>/", views.SoloView.as_view(), name='solo_track'), 
    path("", views.IndexView.as_view(), name="index"),
]
