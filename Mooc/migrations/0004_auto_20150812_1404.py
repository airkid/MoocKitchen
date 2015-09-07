# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mooc', '0003_auto_20150809_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='image_a',
            field=models.FileField(upload_to=b'./Mooc/static/files/quizimg', blank=True),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='image_b',
            field=models.FileField(upload_to=b'./Mooc/static/files/quizimg', blank=True),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='image_c',
            field=models.FileField(upload_to=b'./Mooc/static/files/quizimg', blank=True),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='image_d',
            field=models.FileField(upload_to=b'./Mooc/static/files/quizimg', blank=True),
        ),
        migrations.AddField(
            model_name='quizstore',
            name='visit',
            field=models.BooleanField(default=False),
        ),
    ]
