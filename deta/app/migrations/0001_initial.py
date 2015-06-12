# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('slug', models.SlugField(max_length=10, serialize=False, primary_key=True, blank=True)),
                ('image', pyuploadcare.dj.models.ImageField()),
            ],
        ),
    ]
