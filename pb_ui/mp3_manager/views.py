from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from .models import Track, Playtime
from .form import TrackForm, PlaytimeForm, TrackPlaytimeForm

class IndexView(generic.ListView, FormMixin):
    form_class = TrackForm
    template_name = "mp3_manager/index.html"
    context_object_name = "tracks_list"
 
    def get(self, request):
        print("Getting Track List")
        tracks_list = self.get_queryset()
        playtime = Playtime.objects.all()[0]
        return render(request, self.template_name,
                      {"tracks_list": tracks_list,
                       "form": TrackForm(),
                       "playtimeform": PlaytimeForm(instance=playtime),
                       "trackplaytime": TrackPlaytimeForm()}) 

    def post(self, request):
        print("Handling Track")
        tracks_list = self.get_queryset()
        playtime = Playtime.objects.all()[0]

        if "playtime_update" in request.POST:
            print(f"Updating PlayTime")
            form = PlaytimeForm(request.POST)
            playtime.playtime_seconds = request.POST["playtime_seconds"]
            if form.is_valid():
                obj = form.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=obj),
                               "trackplaytime": TrackPlaytimeForm()})
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=obj),
                               "trackplaytime": TrackPlaytimeForm(),
                               "form_errors": form.errors}) 
        if "track_upload" in request.POST:
            print("Adding track to DB")
            form = self.get_form()

            if form.is_valid():
                form.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm(),
                               "form_errors": form.errors})
        if [key for key in request.POST.keys() if 'trackplaytime_update' in key.lower()]:
            print("Updating track playtime")
            thisform = TrackPlaytimeForm(request.POST)
            if thisform.is_valid():
                print(request.POST)
                track = Track.objects.filter(pk=request.POST["pk"])[0]
                print(track)
                track.playtime_seconds = request.POST["playtime_seconds"]
                track.save()
                
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm(),
                               "form_errors": form.errors})
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Track.objects.order_by()
    
class DeleteView(generic.ListView, FormMixin):
    def get(self, request, pk):
        print(f"DELETING: {pk}")
        Track.objects.filter(pk=pk).delete()
        return redirect("/")
    
class SoloView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"SOLOING: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.solo == False:
            track.solo = True
        else: 
            track.solo = False
        track.save()
        return redirect("/")

class FullView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting full track: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.play_full == False:
            track.play_full = True
        else: 
            track.play_full = False
        track.save()
        return redirect("/")

class OverrideView(generic.ListView, FormMixin):
    
    def get(self, request, pk):
        #get records set solo True and save.
        print(f"Setting playtime override: {pk}")
        track = Track.objects.filter(pk=pk)[0]
        if track.override_playtime == False:
            track.override_playtime = True
        else: 
            track.override_playtime = False
        track.save()
        return redirect("/")

class TrackPlaytimeView(generic.ListView, FormMixin):
    
    def post(self, request, pk):
        #get records set solo True and save.
        print(f"Updating track playtime: {pk}")
        print(request.GET)
        print(request.POST)
        
        track = Track.objects.filter(pk=pk)[0]
        return redirect("/")

        if "trackplaytime_update" in request.POST:
            print("Updating track playtime")
            thisform = TrackPlaytimeForm(request.POST)
            if thisform.is_valid():
                print(request.POST)
                track = Track.objects.filter(pk=request.POST["pk"])[0]
                print(track)
                track.playtime_seconds = request.POST["playtime_seconds"]
                track.save()
                
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm()}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "trackplaytime": TrackPlaytimeForm(),
                               "form_errors": form.errors})
