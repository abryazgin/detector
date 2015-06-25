# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0004_logoobject_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logoobject',
            name='object',
            field=models.TextField(),
        ),
    ]
