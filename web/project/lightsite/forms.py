# -*- coding: utf-8 -*-
from django import forms
from models import UserPhoto


class UserPhotoForm(forms.ModelForm):
    label = u'Выберете фаааааайл'

    class Meta:
        model = UserPhoto
        fields = ['photo']

class UserPhotoUploadFormUpload(forms.ModelForm):
    label = u'Выбеpрете фаайл'
    latest_photo_list = UserPhoto.objects.order_by('-date_create')[:10]
    print (latest_photo_list[0])

    class Meta:
        model = UserPhoto
        fields = ['photo']
