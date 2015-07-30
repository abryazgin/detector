# -*- coding: utf-8 -*-
from django import forms
from models import Photo, CompanyInvite
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['photo']

class CompanyEditForm(forms.ModelForm):

    class Meta:
        model = CompanyInvite
        fields = ['company', 'html']
        widgets = {
           'html':  SummernoteWidget(),
        }



