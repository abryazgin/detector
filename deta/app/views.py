# coding: utf-8
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .models import Image

from django.contrib.auth.decorators import login_required


class UploadView(CreateView):
    model = Image
    fields = []
    
class ImageView(DetailView):
    model = Image
    fields = []
