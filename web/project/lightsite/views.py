from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView

from .models import UserPhoto
from .forms import UserPhotoForm, UserPhotoUploadFormUpload
from UploadProgressCachedHandler import UploadProgressCachedHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError
import json


class MainView(CreateView):
    template_name = 'lightsite/main.html'
    form_class = UserPhotoUploadFormUpload

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            form = UserPhotoUploadFormUpload(request.POST, request.FILES)
            print ("POST", request.FILES, form.is_valid())
            if form.is_valid():
                form.save()
                return HttpResponse("form saved")
            else:
                return HttpResponse("form invalid")

        return HttpResponse("not a ajax request")

class ResultsView(DetailView):
    model = UserPhoto
    template_name = 'lightsite/search.html'

class ListUserPhotoView(ListView):
    template_name = 'lightsite/list_photo.html'
    model = UserPhoto


class CreateUserPhotoView(CreateView):
    template_name = 'lightsite/edit_photo.html'
    form_class = UserPhotoForm

    def get_success_url(self):
        return reverse('userphoto-list')

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST, request.FILES)
        form = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # newdoc = UserPhoto(photo=request.FILES['photo'], name=request.POST["name"])
            # newdoc.save()
            form.save()
            return redirect(self.get_success_url())
        else:
            form = UserPhotoForm()
        return render(request, self.template_name, {'form': form})
