# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0007_auto_20150703_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylogo',
            name='serial_object',
            field=models.TextField(null=True),
        ),
    ]
