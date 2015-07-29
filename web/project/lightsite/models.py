# -*- coding: utf-8 -*-
from django.db import models
from deta.preparer import prepare
from deta.searcher import init
from deta.configManager import Config
from deta.serializer import serialize
from django.conf import settings
from tinymce.models import HTMLField

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return ' '.join([
            self.company.name,
            '-',
            self.user.email,
        ])

class CompanyInvite(models.Model):

    company = models.ForeignKey(Company)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    html = HTMLField(null=True, blank=True)

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

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

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

class LogoStatistic(models.Model):

    #photo = models.ForeignKey(Photo)

    logo = models.ForeignKey(CompanyLogo)

    position = models.IntegerField()

    date_create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return ' '.join([
            self.company.name,
            '-URL:',
            self.photo.url,
            '-POS:',
            self.position,
            '-DATE:',
            self.date_create
        ])
