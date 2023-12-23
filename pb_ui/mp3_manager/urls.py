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
    path("lightupdate/", views.LightUpdate.as_view(), name="lights"),
    path("lightprimary/<int:pk>/", views.LightPrimary.as_view(), name="lightprimary"),
    path("lightfade/<int:pk>/", views.LightFade.as_view(), name="lightfade"),
    path("lightrandom/<int:pk>/", views.LightRandom.as_view(), name="lightrandom"),
    path("lightinterval/<int:pk>/", views.LightInterval.as_view(), name="lightinterval"),
    path("lightalternate/<int:pk>/", views.LightAlternate.as_view(), name="lightalternate"),
    path("lightbrightness/<int:pk>/", views.LightBrightness.as_view(), name="lightbrightness"),
    path("lightbrightnessvalue/", views.LightBrightnessValue.as_view(), name="lightbrightnessvalue"),
    path("lights/", views.BridgeManagement.as_view(), name="bridge"),
    path("disco/", views.DiscoLightManagement.as_view(), name="disco"),
    path("deletedisco/<int:pk>/", views.DeleteDiscoLight.as_view(), name="deletedisco"),
]
