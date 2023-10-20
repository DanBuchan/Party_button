from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from .models import Track
from .form import TrackForm

class IndexView(generic.ListView, FormMixin):
    form_class = TrackForm
    template_name = "mp3_manager/index.html"
    context_object_name = "tracks_list"
 
    def get(self, request):
        tracks_list = self.get_queryset()
        return render(request, self.template_name, {"tracks_list": tracks_list,
                                                    "form": TrackForm()}) 

    def post(self, request):
        tracks_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            form.save()
            return render(request, self.template_name, {"tracks_list": tracks_list,
                                                        "form": TrackForm()}) 
        else:
            return render(request, self.template_name, {"tracks_list": tracks_list,
                                                        "form": TrackForm(),
                                                        "form_errors": form.errors}) 
    

    def get_queryset(self):
        """Return the last five published questions."""
        return Track.objects.order_by()
    
class DeleteView(generic.ListView, FormMixin):
    form_class = TrackForm
    template_name = "mp3_manager/index.html"
    context_object_name = "tracks_list"
 
    def get(self, request, pk):
        Track.objects.filter(pk=pk).delete()
        return redirect("/")