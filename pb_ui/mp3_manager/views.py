from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.conf import settings

import phue
import colorsys
from pydub import AudioSegment
import subprocess
import re
import pprint
from subprocess import Popen, PIPE

from .models import Track, Playtime, Playlist, Bridge, Light, DiscoLight
from .form import TrackForm, PlaytimeForm, TrackPlaytimeForm, TrackStartForm
from .form import BridgeForm, TrackForm ,TrackBpmForm
from .form import PlaylistForm, BrightnessForm, DiscoForm


class DiscoLightManagement(generic.ListView, FormMixin):
    form_class = DiscoForm
    template_name = "mp3_manager/disco.html"
    context_object_name = "disco_light_list"
    model = DiscoLight

    def get(self, request):
        print("Getting Disco Light List")
        disco_light_list = self.get_queryset()
        return render(request, self.template_name,
                      {"disco_light_list": disco_light_list,
                       "form": DiscoForm()
                       })
        
    def post(self, request):
        print("Handling Disco Light")
        if "disco_configure" in request.POST:
            print("Adding Disco Light Configuration")
            form = self.get_form()
            if form.is_valid():
                print("SAVING LIGHT")
                record = form.save()

            disco_light_list = self.get_queryset()
            return render(request, self.template_name,
                          {"disco_light_list": disco_light_list,
                           "form": DiscoForm()
                          })
        if [key for key in request.POST.keys() if 'disco_update' in key.lower()]:
            print("Updating Disco Light")
            thisform = DiscoForm(request.POST)
            if thisform.is_valid():
                light = DiscoLight.objects.filter(pk=request.POST["pk"])[0]
            #print(request.POST)
            light.name = request.POST["name"]
            light.pin_id = request.POST["pin_id"]
            toggle_list = request.POST.getlist("light_on")
            if len(toggle_list) > 0:
                light.light_on = True
            else:
                light.light_on = False
            light.save()
            disco_light_list = self.get_queryset()
            return render(request, self.template_name,
                          {"disco_light_list": disco_light_list,
                           "form": DiscoForm()
                          })


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
                #command = ['/opt/homebrew/Cellar/bpm-tools/0.3/bin/bpm-tag',
                command = ['/usr/bin/bpm-tag',
                           '-f',
                           '-n',
                           f"{str(settings.BASE_DIR)}/{str(record.mp3_file)}",
                           ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = result.stderr.decode('utf-8')
                
                # look for: Trackpath: 146.000 BPM
                x = re.search("\s(\d+)\.\d+\sBPM", output)
                if x:
                    for match in x.groups():
                        record.bpm = int(match)
                audio_file = AudioSegment.from_file(f"{str(settings.BASE_DIR)}/{str(record.mp3_file)}")
                duration = audio_file.duration_seconds
                record.mp3_length = duration*1000
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
        playtime = Playtime.objects.all()
        if not playtime:
            playlist = Playlist.objects.create(name="default")
            playtime = Playtime.objects.create(playlist_selection=playlist)
        else:
            playtime = playtime[0]
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
            if playtime.music_only == True:
                playtime.music_only = False
                playtime.lights_only = False
            else:
                playtime.music_only = True
                if playtime.lights_only == True:
                    playtime.lights_only = False
            playtime.save()
            return redirect("/")
        if "ghostctl_submit" in request.POST:
            if playtime.ghost == True:
                playtime.ghost = False
            else:
                playtime.ghost = True
            playtime.save()
            cmd = ['/usr/bin/sudo', '/usr/bin/systemctl', 'restart', 'party_button']
            print(f'RESTARTING PARTY SERVICE: {" ".join(cmd)}')
            p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            return redirect("/")
        
class DeleteTrackView(generic.ListView, FormMixin):
    def get(self, request, pk):
        print(f"DELETING TRACK: {pk}")
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
        lights = Light.objects.all().order_by('name')
        return render(request, self.template_name,
                      {"bridge": bridge,
                       "lights": lights,
                       "bridgeform": BridgeForm(instance=bridge),
                       "brightnessform": BrightnessForm(instance=bridge),
                       }) 

    def post(self, request):
        print(request.POST)
        if "bridge_reset" in request.POST:
            Light.objects.all().delete()
            form = BridgeForm(request.POST)
            if form.is_valid():
                bridge = Bridge.objects.all().first()
                if bridge:
                    bridge.ip = request.POST["ip"]
                    bridge.user_id = request.POST["user_id"]
                    bridge.name_stub = request.POST["name_stub"]
                    bridge.room = request.POST["room"]
                else:
                    bridge = Bridge.objects.create(ip = request.POST["ip"],
                                                   user_id = request.POST["user_id"],
                                                   name_stub = request.POST["name_stub"],
                                                   room = request.POST["room"])
                obj = bridge.save()
                try:
                    b = phue.Bridge(bridge.ip, bridge.user_id)
                    lights = b.get_api()["lights"]
                    # pprint.pprint(b.get_api()["lights"])

                    for light_id in lights:
                        light = lights[light_id]
                        if bridge.name_stub in light["name"]:
                            # print(light_id, light["name"], light["state"]["hue"],
                            #       light["state"]["sat"],  light["state"]["bri"])
                            h = light["state"]["hue"]/65535
                            s = light["state"]["sat"]/254
                            v = light["state"]["bri"]/254
                            rgb_values = colorsys.hsv_to_rgb(h, s, v)
                            r = int(254*rgb_values[0])
                            g = int(254*rgb_values[1])
                            b = int(254*rgb_values[2])
                            light_obj = Light.objects.create(name=light["name"],
                                                             hue_bridge_id = light_id,
                                                             primary_R=r, 
                                                             primary_G=g, 
                                                             primary_B=b, 
                                                             secondary_R=r, 
                                                             secondary_G=g, 
                                                             secondary_B=b, 
                                                             primary_H=light["state"]["hue"], 
                                                             primary_S=light["state"]["sat"], 
                                                             primary_V=light["state"]["bri"], 
                                                             secondary_H= light["state"]["hue"], 
                                                             secondary_S=light["state"]["sat"], 
                                                             secondary_V=light["state"]["bri"], 
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
        light.random_interval=False
        light.randomise_brightness=False
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
        light.random_interval=False
        light.randomise_brightness=False
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
        light.randomise_brightness=False
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
            if light.fade or light.primary_colour:
                light.random_interval=False
            else:
                light.random_interval=True
                
        light.save()
        return redirect("/lights")

class LightBrightness(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting brightness override for: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        if light.override_brightness:
            light.override_brightness=False
        else:
            light.override_brightness=True   
            light.randomise_brightness=False   
        light.save()
        return redirect("/lights")
    
class LightBrightnessValue(generic.ListView, FormMixin):
    
    def post(self, request):
        #get records set solo True and save.
        pk = request.POST["pk"]
        print(request.POST)
        print(f"Setting brightness override for: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        light.brightness=request.POST['brightness']     
        light.save()
        return redirect("/lights")
    
class LightRandBri(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        print(f"Setting brightness to randomise: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        if light.randomise_brightness:
            light.randomise_brightness=False
        else:
            if light.random_colour:
                light.randomise_brightness=True
                light.override_brightness=False
             
        light.save()
        return redirect("/lights")

class LightOff(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        print(f"Setting Light Off: {pk}")
        light = Light.objects.filter(pk=pk)[0]
        if light.off:
            light.off=False
        else:
            light.off=True
             
        light.save()
        return redirect("/lights") 

class DeleteDiscoLight(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        print(f"DELETING DISCO LIGHT: {pk}")
        DiscoLight.objects.filter(pk=pk).delete()
        return redirect("/disco")