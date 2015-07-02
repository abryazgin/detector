# coding: utf-8
from django.db import models
from os.path import abspath
from django.contrib.auth.models import User 

class Image(models.Model):
    image = models.ImageField(upload_to='app/static/images')
    insert_datetime = models.DateTimeField()
    
    def image_abs_path (self):
      return abspath(str(self.image).decode('utf-8'))
    
    def imgsrc (self):
      return u'<img src="%s" width="100" height="100"  />' % self.image_abs_path()
    imgsrc.allow_tags = True

class Company(models.Model):
    name = models.CharField(max_length = 100)
    
class Logo(models.Model):
    company = models.ForeignKey(Company)
    image = models.ForeignKey(Image)    
    
class PrepareImage(models.Model):
    image = models.ForeignKey(Image)
    
    
'''
from app.models import Image
img = Image.objects.get(pk=2) 
img.imgsrc()
''' 