# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0010_auto_20150728_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='logostatistic',
            name='go_to_company',
            field=models.BooleanField(default=False),
        ),
    ]
