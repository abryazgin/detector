# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, TemplateView

from .models import Photo
from .forms import PhotoForm, PhotoUploadFormUpload
from UploadProgressCachedHandler import UploadProgressCachedHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import RequestContext
import json


class MainView(CreateView):
    template_name = 'lightsite/main.html'
    form_class = PhotoUploadFormUpload


    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            print("%s?name=joe" % reverse("search"))
            form = PhotoUploadFormUpload(request.POST, request.FILES)
            print ("POST", request.FILES, form.is_valid())
            if form.is_valid():
                new_photo = form.save()
                return HttpResponse(
                    json.dumps({'response': reverse('search', args=(new_photo.pk,)),
                                'result': 'success'}))
                # return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponse(
                    json.dumps({'response': u"Скорее всего Вы выбрали файл с неподходящим форматом.",
                                'result': 'error'}))

        return HttpResponse("not a ajax request")

class SearchView(TemplateView):
     template_name = 'lightsite/search.html'

     def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        photo_id = self.kwargs.get('photo_id', None)
        print('photo_id', photo_id)
        if (photo_id):
            try:
                context['photo'] = Photo.objects.get(pk=photo_id)
            except (KeyError, Photo.DoesNotExist):
                print ('Photo.DoesNotExist')
        return context

class ListPhotoView(ListView):
    template_name = 'lightsite/list_photo.html'
    model = Photo


class CreatePhotoView(CreateView):
    template_name = 'lightsite/edit_photo.html'
    form_class = PhotoForm

    def get_success_url(self):
        return reverse('userphoto-list')

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST, request.FILES)
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # newdoc = Photo(photo=request.FILES['photo'], name=request.POST["name"])
            # newdoc.save()
            form.save()
            return redirect(self.get_success_url())
        else:
            form = PhotoForm()
        return render(request, self.template_name, {'form': form})
