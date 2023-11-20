from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.conf import settings

import librosa
import phue
import colorsys

from .models import Track, Playtime, Playlist, Bridge, Light
from .form import TrackForm, PlaytimeForm, TrackPlaytimeForm, TrackStartForm
from .form import BridgeForm, TrackForm ,TrackBpmForm
from .form import PlaylistForm, BrightnessForm

class TrackManagement(generic.ListView, FormMixin):
    form_class = TrackForm
    template_name = "mp3_manager/track.html"
    context_object_name = "tracks_list"
    model = Track

    def get(self, request):
        tracks_list = None
        print("Getting Track List")
        tracks_list = self.get_queryset()
        return render(request, self.template_name,
                      {"tracks_list": tracks_list,
                       "form": TrackForm(),
                       "trackplaytime": TrackPlaytimeForm(),
                       "trackbpmform": TrackBpmForm()})

    def post(self, request):
        print("Handling Track")
        tracks_list = self.get_queryset()

        if "track_upload" in request.POST:
            print("Adding track to DB")
            form = self.get_form()
            if form.is_valid():
                record = form.save()
                audio_file = librosa.load(f"{str(settings.BASE_DIR)}/{str(record.mp3_file)}")
                y, sr = audio_file
                tempo = librosa.feature.tempo(y=y, sr=sr)
                record.bpm = tempo[0]
                record.mp3_length = librosa.get_duration(y=y, sr=sr)*1000
                record.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm(),
                               "form_errors": form.errors})#
        if [key for key in request.POST.keys() if 'trackbpm_update' in key.lower()]:
            print("Updating BPM")
            thisform = TrackBpmForm(request.POST)
            if thisform.is_valid():
                track = Track.objects.filter(pk=request.POST["pk"])[0]
                track.bpm = request.POST["bpm"]
                track.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm(),
                               "form_errors": thisform.errors})
        if [key for key in request.POST.keys() if 'trackplaytime_update' in key.lower()]:
            print("Updating track playtime")
            thisform = TrackPlaytimeForm(request.POST)
            if thisform.is_valid():
                track = Track.objects.filter(pk=request.POST["pk"])[0]
                track.playtime_seconds = request.POST["playtime_seconds"]
                track.save()
                
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm(),
                               "form_errors": thisform.errors})
        if [key for key in request.POST.keys() if 'trackstart_update' in key.lower()]:
            print("Updating track start")
            thisform = TrackStartForm(request.POST)
            if thisform.is_valid():
                track = Track.objects.filter(pk=request.POST["pk"])[0]
                track.minutes = request.POST["minutes"]
                track.seconds = request.POST["seconds"]
                track.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "trackplaytime": TrackPlaytimeForm(),
                               "trackbpmform": TrackBpmForm(),
                               "form_errors": thisform.errors})

class PlaylistManagement(generic.ListView, FormMixin):
    template_name = "mp3_manager/playlist.html"
    context_object_name = "playlist_list"
    model = Playlist
    form_class = PlaylistForm

    def get(self, request):
        playlist_list = self.get_queryset()
        tracklist = Track.objects.all()
        return render(request, self.template_name,
                      {"playlist_list": playlist_list,
                       "tracklist": tracklist,
                       "playlistform": PlaylistForm})
    
    def post(self, request):
        print("Handling playlist")
        playlist_list = self.get_queryset()
        tracklist = Track.objects.all()
        print(request.POST)
        if "addplaylist_submit" in request.POST:
            form = self.get_form()
            if form.is_valid():
                form.save()
                playlist_list = self.get_queryset()
                return render(request, self.template_name,
                              {"playlist_list": playlist_list,
                              "tracklist": tracklist,
                              "playlistform": PlaylistForm})
            else:
                return render(request, self.template_name,
                              {"playlist_list": playlist_list,
                              "playlistform": PlaylistForm,
                              "tracklist": tracklist,
                              "form_errors": form.errors})
        if "removeplaylist_submit" in request.POST:
            Playlist.objects.filter(pk=request.POST['playlist_selection']).delete()
            return redirect("/playlists")
        if "assignplaylist_submit" in request.POST:
            track = Track.objects.filter(pk=request.POST['track_selection'])[0]
            playlist = Playlist.objects.filter(pk=request.POST['playlist_selection'])[0]
            track.playlists.add(playlist)
            track.save()
            return render(request, self.template_name,
                          {"playlist_list": playlist_list,
                          "tracklist": tracklist,
                          "playlistform": PlaylistForm})
        if [key for key in request.POST.keys() if 'unassignplaylist_submit' in key.lower()]:
            track = Track.objects.filter(pk=request.POST['track_pk'])[0]
            playlist = Playlist.objects.filter(pk=request.POST['playlist_pk'])[0]
            track.playlists.remove(playlist)
            playlist_list = self.get_queryset()
            return render(request, self.template_name,
                          {"playlist_list": playlist_list,
                          "tracklist": tracklist,
                          "playlistform": PlaylistForm})
            
        
class IndexView(generic.ListView, FormMixin):
    form_class = PlaytimeForm
    template_name = "mp3_manager/index.html"
    context_object_name = "tracks_list"
  
    def get(self, request):
        playlists = Playlist.objects.all()
        playtime = Playtime.objects.all()[0]
        return render(request, self.template_name,
                      {"playtime": playtime,
                       "playtimeform": PlaytimeForm(instance=playtime),
                       "playlists": playlists}) 

    def post(self, request):
        print("Handling Playtime")
        playtime = Playtime.objects.all()[0]
        playlists = Playlist.objects.all()
        # print(request.POST)
        if "playtime_update" in request.POST:
            print(f"Updating PlayTime")
            form = PlaytimeForm(request.POST)
            playtime.playtime_seconds = request.POST["playtime_seconds"]
            if form.is_valid():
                obj = form.save()
                obj.playlist_selection =  playtime.playlist_selection
                obj.save()
                return render(request, self.template_name,
                              {"playtime": playtime,
                               "playtimeform": PlaytimeForm(instance=obj),
                               "playlists": playlists})
            else:
                return render(request, self.template_name,
                              {"playtime": playtime,
                               "playtimeform": PlaytimeForm(instance=obj),
                               "form_errors": form.errors,
                               "playlists": playlists})
        if "selectplaylist_submit" in request.POST:
            playlist = Playlist.objects.filter(pk=request.POST['playlist_selection'])[0]
            playtime.playlist_selection = playlist
            playtime.save()
            return redirect("/")
        if "lightsctl_submit" in request.POST:
            if playtime.lights_only == True:
                playtime.lights_only = False
                playtime.music_only = False
            else:
                playtime.lights_only = True
                if playtime.music_only == True:
                    playtime.music_only = False
            playtime.save()
            return redirect("/")
        if "musicctl_submit" in request.POST:
            print("hi")
            if playtime.music_only == True:
                playtime.music_only = False
                playtime.lights_only = False
            else:
                playtime.music_only = True
                if playtime.lights_only == True:
                    playtime.lights_only = False
            playtime.save()
            return redirect("/")
        
            
    
class DeleteTrackView(generic.ListView, FormMixin):
    def get(self, request, pk):
        print(f"DELETING: {pk}")
        Track.objects.filter(pk=pk).delete()
        return redirect("/tracks")
 
class SoloTrackView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"SOLOING: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.solo == False:
            track.solo = True
        else: 
            track.solo = False
        track.save()
        return redirect("/tracks")

class FullTrackView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting full track: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.play_full == False:
            track.play_full = True
        else: 
            track.play_full = False
        track.save()
        return redirect("/tracks")

class OverrideTrackView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting playtime override: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.override_playtime == False:
            track.override_playtime = True
        else: 
            track.override_playtime = False
        track.save()
        return redirect("/tracks")

class TrackPlaytimeView(generic.ListView, FormMixin):
    
    def post(self, request, pk):
        #get records set solo True and save.
        print(f"Updating track playtime: {pk}")
        print(request.GET)
        print(request.POST)
        
        track = Track.objects.filter(pk=pk)[0]
        return redirect("/tracks")

class BridgeManagement(generic.ListView, FormMixin):
    template_name = "mp3_manager/lights.html"
    model = Bridge
    form_class = BridgeForm

    def get(self, request):
        bridge = Bridge.objects.all().first()
        lights = Light.objects.all()
        return render(request, self.template_name,
                      {"bridge": bridge,
                       "lights": lights,
                       "bridgeform": BridgeForm(instance=bridge),
                       "brightnessform": BrightnessForm(instance=bridge),
                       }) 

    def post(self, request):
        # print(request.POST)
        if "bridge_reset" in request.POST:
            Light.objects.all().delete()
            form = BridgeForm(request.POST)
            if form.is_valid():
                bridge = Bridge.objects.all().first()
                bridge.ip = request.POST["ip"]
                bridge.user_id = request.POST["user_id"]
                bridge.name_stub = request.POST["name_stub"]
                obj = bridge.save()
                try: 
                    b = phue.Bridge(bridge.ip, bridge.user_id)
                    light_list = []
                    for light in b.lights:
                        if bridge.name_stub in light.name:
                            light_list.append(light)
                    for light in light_list:
                        print(light.name, light.hue, light.saturation, light.brightness)
                        h = light.hue/65535
                        s = light.saturation/254
                        v = light.brightness/254
                        rgb_values = colorsys.hsv_to_rgb(h, s, v)
                        r = int(254*rgb_values[0])
                        g = int(254*rgb_values[1])
                        b = int(254*rgb_values[2])
                        light_obj = Light.objects.create(name=light.name,
                                                         primary_R=r, 
                                                         primary_G=g, 
                                                         primary_B=b, 
                                                         secondary_R=r, 
                                                         secondary_G=g, 
                                                         secondary_B=b, 
                                                         primary_H=light.hue, 
                                                         primary_S=light.saturation, 
                                                         primary_V=light.brightness, 
                                                         secondary_H=light.hue, 
                                                         secondary_S=light.saturation, 
                                                         secondary_V=light.brightness, 
                                                         )
                except Exception as e:
                    print("CAN'T FIND BRIDGE: "+str(e))

             # find all lights that match tubs
             # save light record fo each
        if "brightness_update" in request.POST:
            form = BrightnessForm(request.POST)
            if form.is_valid():
                bridge = Bridge.objects.all().first()
                bridge.brightness = request.POST["brightness"]
                bridge.save()
        return redirect("/lights")


class LightUpdate(generic.ListView, FormMixin):
    template_name = "mp3_manager/lights.html"

    def post(self, request):
        print(request.POST)
        if [key for key in request.POST.keys() if 'light_update' in key.lower()]:
            # Should really check this validates with the lightForm
            light = Light.objects.filter(pk=request.POST['pk'])[0]
            light.primary_R=int(request.POST['primary_R'])
            light.primary_G=int(request.POST['primary_G'])
            light.primary_B=int(request.POST['primary_B'])
            light.secondary_R=int(request.POST['secondary_R'])
            light.secondary_G=int(request.POST['secondary_G'])
            light.secondary_B=int(request.POST['secondary_B'])
            light.interval_size=int(request.POST['interval_size'])
            hsv_values = colorsys.rgb_to_hsv(light.primary_R/254, light.primary_G/254, light.primary_B/254)
            h = int(65535 * hsv_values[0])
            s = int(254 * hsv_values[1])
            v = int(254 * hsv_values[2])
            light.primary_H=h 
            light.primary_S=s
            light.primary_V=v
            hsv_values = colorsys.rgb_to_hsv(light.secondary_R/254, light.secondary_G/254, light.secondary_B/254)
            h = int(65535 * hsv_values[0])
            s = int(254 * hsv_values[1])
            v = int(254 * hsv_values[2])
            light.secondary_H=h
            light.secondary_S=s
            light.secondary_V=s
            light.save()
        return redirect("/lights")
    
class LightPrimary(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting Light to primary colour only: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        light.primary_colour = True
        light.fade = False
        light.random_colour = False
        light.alternate_colour = False
        light.save()
        return redirect("/lights")

class LightFade(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting Light to fade: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        light.primary_colour = False
        light.fade = True
        light.random_colour = False
        light.alternate_colour = False
        light.save()
        return redirect("/lights")

class LightRandom(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting Light to random: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        light.primary_colour = False
        light.fade = False
        light.random_colour = True
        light.alternate_colour = False
        light.save()
        return redirect("/lights")

class LightAlternate(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting Light to alternate: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        light.primary_colour = False
        light.fade = False
        light.random_colour = False
        light.alternate_colour = True
        light.save()
        return redirect("/lights")


class LightInterval(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting Change interval to random: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        if light.random_interval:
            light.random_interval=False
        else:
            light.random_interval=True
        light.save()
        return redirect("/lights")
