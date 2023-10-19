from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import track
from .form import TrackForm

class IndexView(generic.ListView):
    form_class = TrackForm
    template_name = "mp3_manager/index.html"
    context_object_name = "tracks_list"
 
    def get_queryset(self):
        """Return the last five published questions."""
        return track.objects.order_by()
    
    def get_context_data(self,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['form'] = TrackForm()
        return context

class UploadView(generic.DetailView):
    form_class = TrackForm
    model = track
    template_name = "mp3_manager/index.html"

class DeleteView(generic.DetailView):
    form_class = TrackForm
    model = track
    template_name = "mp3_manager/index.html"
