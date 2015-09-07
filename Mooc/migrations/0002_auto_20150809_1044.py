# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mooc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='gap_hour',
        ),
        migrations.AddField(
            model_name='unit',
            name='gap_days',
            field=models.IntegerField(default=24),
        ),
    ]
