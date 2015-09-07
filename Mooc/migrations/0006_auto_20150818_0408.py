# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mooc', '0005_auto_20150815_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='announcement',
            field=models.CharField(default='\u6682\u65e0\u516c\u544a', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='studystatus',
            name='last_section',
            field=models.IntegerField(default=1, blank=True),
        ),
    ]
