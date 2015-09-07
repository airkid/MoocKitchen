# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mooc', '0004_auto_20150812_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='ppt',
        ),
        migrations.AddField(
            model_name='section',
            name='pdf',
            field=models.FileField(null=True, upload_to=b'./Mooc/static/files/pdf', blank=True),
        ),
    ]
