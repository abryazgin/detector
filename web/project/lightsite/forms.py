# -*- coding: utf-8 -*-
from django import forms
from models import Photo, CompanyInvite
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['photo']

class CompanyEditForm(forms.ModelForm):

    html = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 10}))

    class Meta:
        model = CompanyInvite
        fields = ['company', 'html']



