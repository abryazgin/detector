# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, TemplateView

from .models import Photo
from .forms import PhotoForm
from UploadProgressCachedHandler import UploadProgressCachedHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import RequestContext
import json, urllib, os
from deta import runner
from django.conf import settings



class MainView(TemplateView):
    template_name = 'lightsite/main.html'


def check_image_from_ajax(request):
    form = PhotoForm(request.POST, request.FILES)
    print ("check_image_from_ajax", request.FILES, form.is_valid())
    if form.is_valid():
        return HttpResponse(
            json.dumps({
                'result': 'success'}))
    else:
        return HttpResponse(
            json.dumps({'data': u"Скорее всего Вы выбрали файл с неподходящим форматом.",
                        'result': 'error'}))

def get_media_path(abspath):
    return abspath.replace(settings.BASE_DIR, '', 1)

def search_logo_from_ajax(request):
    logo = [{'imgPath': get_media_path(result.logoImg)} for result in
            runner.runAll(request.FILES['photo'], None, 2)]
    print ('logo', logo)
    context = {
        "logo": logo,
    };

    return render_to_response("lightsite/finded_logo_snippet.html",
                          context)


def get_prev_photo_from_ajax(request):
    latest_photo_list = Photo.objects.order_by('-date_create')[:20]
    context = {
        "latest_photo_list": latest_photo_list,
        "MEDIA_URL": settings.MEDIA_URL,
    }
    return render_to_response("lightsite/prev_photo_snippet.html",
                              context)


class SearchView(TemplateView):
    template_name = 'lightsite/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        print('search', self.request.POST, self.kwargs)
        photo_id = self.kwargs.get('pk', None)
        print('photo_id', photo_id)
        if (photo_id):
            try:
                context['photo'] = Photo.objects.get(pk=photo_id).photo
            except (KeyError, Photo.DoesNotExist):
                print ('Photo.DoesNotExist')
        return context

    def find_logo(self, photoPath):
        return [{'imgPath': get_media_path(result.logoImg)} for result in runner.runAll(photoPath, 2)]

    def get_not_exist_url(self):
        return reverse('main')

    def post(self, request, *args, **kwargs):
        print ('POST', request.POST, request.GET)
        photo_pk = request.POST.get('pk', None)
        return HttpResponseRedirect(reverse('search-done', args=(photo_pk,)))

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
