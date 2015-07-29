# -*- coding: utf-8 -*-
from django import forms
from models import Photo, CompanyInvite
from ckeditor.widgets import CKEditorWidget

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['photo']

class CompanyEditForm(forms.ModelForm):

    html = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CompanyInvite
        fields = ['company', 'html']



