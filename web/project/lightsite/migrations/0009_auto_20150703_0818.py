# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0008_auto_20150703_0718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companylogo',
            name='serial_object',
        ),
        migrations.AddField(
            model_name='companylogo',
            name='serial_desc_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='companylogo',
            name='serial_kp_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
