from django.urls import path
from . import views

app_name = "mp3_manager"
urlpatterns = [
    path("deletetrack/<int:pk>/", views.DeleteTrackView.as_view(), name='delete_track'), 
    path("solotrack/<int:pk>/", views.SoloTrackView.as_view(), name='solo_track'), 
    path("playfulltrack/<int:pk>/", views.FullTrackView.as_view(), name='play_full'), 
    path("overridetrack/<int:pk>/", views.OverrideTrackView.as_view(), name='override'), 
    path("trackplaytime/", views.TrackPlaytimeView.as_view(), name='track_playtime'), 
    path("selectplaylist/", views.IndexView.as_view(), name='selectplaylist'), 
    path("", views.IndexView.as_view(), name="index"),
    path("tracks/", views.TrackManagement.as_view(), name="tracks"),
    path("playlists/", views.PlaylistManagement.as_view(), name="playlists"),
    path("addplaylist/", views.PlaylistManagement.as_view(), name="addplaylist"),
    path("removeplaylist/", views.PlaylistManagement.as_view(), name="removeplaylist"),
    path("assignplaylist/", views.PlaylistManagement.as_view(), name="assignplaylist"),    
    path("unassignplaylist/", views.PlaylistManagement.as_view(), name="unassignplaylist"),    
]
