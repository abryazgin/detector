# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0011_logostatistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinvite',
            name='html',
            field=tinymce.models.HTMLField(null=True, blank=True),
        ),
    ]
