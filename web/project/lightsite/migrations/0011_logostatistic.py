# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightsite', '0010_auto_20150728_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ForeignKey(to='lightsite.CompanyLogo')),
            ],
        ),
    ]
