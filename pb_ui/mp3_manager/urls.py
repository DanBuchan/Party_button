from django.urls import path
from . import views

app_name = "mp3_manager"
urlpatterns = [
    path("delete/<int:pk>/", views.DeleteView.as_view(), name='delete_track'), 
    path("solo/<int:pk>/", views.SoloView.as_view(), name='solo_track'), 
    path("playfull/<int:pk>/", views.FullView.as_view(), name='play_full'), 
    path("override/<int:pk>/", views.OverrideView.as_view(), name='override'), 
    path("", views.IndexView.as_view(), name="index"),

]
