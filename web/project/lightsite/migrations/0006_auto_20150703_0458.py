# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0005_auto_20150630_0448'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPhoto',
            new_name='Photo',
        ),
    ]
