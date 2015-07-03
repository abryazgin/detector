# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField

# Create your models here.
class Photo(models.Model):

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    photo = models.ImageField(
        upload_to='photos'
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
        upload_to='logo'
    )

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __unicode__(self):

         return ' '.join([
            self.company.name,
            '-',
            self.photo.url,
        ])
class LogoObject(models.Model):

    logo = models.ForeignKey(CompanyLogo)

    object = models.TextField()

    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __unicode__(self):
        return ' '.join([
            self.logo.company.name,
            '-',
            self.logo.photo.url,
        ])