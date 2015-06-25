# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0002_auto_20150629_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'logo')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='lightsite.Company')),
                ('creator', models.ForeignKey(to='lightsite.User')),
            ],
        ),
        migrations.CreateModel(
            name='LogoObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ForeignKey(to='lightsite.CompanyLogo')),
            ],
        ),
        migrations.RemoveField(
            model_name='companylogos',
            name='company',
        ),
        migrations.RemoveField(
            model_name='companylogos',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='logoobjects',
            name='logo',
        ),
        migrations.DeleteModel(
            name='CompanyLogos',
        ),
        migrations.DeleteModel(
            name='LogoObjects',
        ),
    ]
