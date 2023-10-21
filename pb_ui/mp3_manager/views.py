from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from .models import Track, Playtime
from .form import TrackForm, PlaytimeForm

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
                       "playtimeform": PlaytimeForm(instance=playtime),}) 

    def post(self, request):
        print("Adding Track")
        tracks_list = self.get_queryset()
        playtime = Playtime.objects.all()[0]
        if "playtime_update" in request.POST:
            print(f"Updating PlayTime:  seconds")
            form = PlaytimeForm(request.POST)
            if form.is_valid():
                playtime.playtime_seconds = request.POST["playtime_seconds"]
                playtime.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime)})
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
                               "form_errors": form.errors}) 
        if "track_upload" in request.POST:
            print("Adding track to DB")
            form = self.get_form()

            if form.is_valid():
                form.save()
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),}) 
            else:
                return render(request, self.template_name,
                              {"tracks_list": tracks_list,
                               "form": TrackForm(),
                               "playtimeform": PlaytimeForm(instance=playtime),
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
