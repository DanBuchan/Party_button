from django.urls import path
from . import views

app_name = "mp3_manager"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("delete/<int:pk>/", views.DeleteView.as_view(), name='delete_track'), 
]
