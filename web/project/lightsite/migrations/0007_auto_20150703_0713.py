# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0006_auto_20150703_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logoobject',
            name='logo',
        ),
        migrations.AddField(
            model_name='companylogo',
            name='serial_object',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companylogo',
            name='photo',
            field=models.ImageField(upload_to=b'logos'),
        ),
        migrations.DeleteModel(
            name='LogoObject',
        ),
    ]
