# -*- coding: utf-8 -*-
from django import forms
from models import Photo


class PhotoForm(forms.ModelForm):
    label = u'Выберете фаааааайл'

    class Meta:
        model = Photo
        fields = ['photo']

class PhotoUploadFormUpload(forms.ModelForm):
    label = u'Выбеpрете фаайл'
    latest_photo_list = Photo.objects.order_by('-date_create')[:20]

    class Meta:
        model = Photo
        fields = ['photo']
