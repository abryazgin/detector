# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_change', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='lightsite.Company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyLogos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'logo')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='lightsite.Company')),
            ],
        ),
        migrations.CreateModel(
            name='LogoObjects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ForeignKey(to='lightsite.CompanyLogos')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='lightsite.Company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userphoto',
            name='name',
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='photo',
            field=models.ImageField(upload_to=b'photos'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(to='lightsite.User'),
        ),
        migrations.AddField(
            model_name='companylogos',
            name='creator',
            field=models.ForeignKey(to='lightsite.User'),
        ),
        migrations.AddField(
            model_name='companyinvite',
            name='creator',
            field=models.ForeignKey(to='lightsite.User'),
        ),
    ]
