# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mooc', '0002_auto_20150809_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='gap_days',
            field=models.IntegerField(default=1),
        ),
    ]
