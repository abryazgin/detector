# -*- coding: utf-8 -*-
from django.db import models
from deta.preparer import prepare
from deta.searcher import init
from deta.configManager import Config
from deta.serializer import serialize
from django.conf import settings
import uuid
import os

# Create your models here.
class Photo(models.Model):

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    photo = models.ImageField(
        upload_to=settings.PHOTO_DIRNAME
    )

    def __unicode__(self):
        return ' '.join([
            self.photo.name,
        ])

class User(models.Model):

    login = models.CharField(
        max_length=50,
    )

    password = models.CharField(
        max_length=50,
    )

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.login

class Company(models.Model):

    name = models.CharField(
        max_length=50,
    )

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.name

class Staff(models.Model):

    company = models.ForeignKey(Company)

    user = models.ForeignKey(User)

    def __unicode__(self):
        return ' '.join([
            self.company.name,
            '-',
            self.user.login,
        ])

class CompanyInvite(models.Model):

    company = models.ForeignKey(Company)

    creator = models.ForeignKey(User)

    html = models.TextField()

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    date_change = models.DateTimeField(
        auto_now=True,
    )

    def __unicode__(self):
        return self.company.name

class CompanyLogo(models.Model):

    company = models.ForeignKey(Company)

    creator = models.ForeignKey(User)

    photo = models.ImageField(
        upload_to=settings.LOGO_DIRNAME
    )

    date_create = models.DateTimeField(
        auto_now_add=True,
    )
    
    serial_kp_file = models.FileField (blank=True, null=True)
    serial_desc_file = models.FileField (blank=True, null=True)

    def __unicode__(self):
        return ' '.join([
            self.company.name,
            '-',
            self.photo.url,
        ])
    
    def save(self, *args, **kwargs):
        super(CompanyLogo, self).save(*args, **kwargs)
        detector, matcher = init()
        
        kp, desc = prepare(os.path.join(settings.MEDIA_ROOT,self.photo.name), detector, int(Config.get('LOGOS','w')), int(Config.get('LOGOS','h')))
        uid = uuid.uuid4()
        kp_filepath = os.path.join(settings.MEDIA_ROOT,settings.SERIAL_DIRNAME,'kp_{}.pick'.format(uid))
        desc_filepath = os.path.join(settings.MEDIA_ROOT,settings.SERIAL_DIRNAME,'desc_{}.pick'.format(uid))
        self.serial_kp_file = serialize(kp,kp_filepath)
        self.serial_desc_file = serialize(desc,desc_filepath)
        super(CompanyLogo, self).save(*args, **kwargs)
