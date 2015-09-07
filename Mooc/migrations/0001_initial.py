# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('summary', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('begin_time', models.DateTimeField()),
                ('course', models.ForeignKey(related_name='times', to='Mooc.Course')),
                ('cur_course', models.OneToOneField(related_name='cur_time', null=True, blank=True, to='Mooc.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('option_a', models.CharField(default=b'A', max_length=10)),
                ('option_b', models.CharField(default=b'B', max_length=10)),
                ('option_c', models.CharField(default=b'C', max_length=10)),
                ('option_d', models.CharField(default=b'D', max_length=10)),
                ('answer', models.CharField(max_length=30)),
                ('counter', models.IntegerField()),
                ('image', models.FileField(upload_to=b'./Mooc/static/files/quizimg', blank=True)),
                ('user_answer', models.CharField(max_length=10, blank=True)),
                ('question_score', models.IntegerField(default=5, blank=True)),
                ('question_type', models.CharField(max_length=10, choices=[(b'0', '\u5224\u65ad\u9898'), (b'1', '\u9009\u62e9\u9898'), (b'2', '\u7b80\u7b54\u9898')])),
                ('quiz', models.ForeignKey(related_name='questions', to='Mooc.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_counter', models.IntegerField()),
                ('section_counter', models.IntegerField()),
                ('Answer', models.CharField(default=b'', max_length=50)),
                ('score', models.IntegerField(default=0, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('video', models.FileField(null=True, upload_to=b'./Mooc/static/files/video', blank=True)),
                ('ppt', models.FileField(null=True, upload_to=b'./Mooc/static/files/ppt', blank=True)),
                ('counter', models.IntegerField()),
                ('total_counter', models.IntegerField(default=0)),
                ('begin', models.IntegerField(default=0)),
                ('course', models.ForeignKey(related_name='sections', to='Mooc.Course')),
                ('quiz', models.OneToOneField(related_name='section', null=True, blank=True, to='Mooc.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='StudyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(related_name='status', to='Mooc.Course')),
                ('course_time', models.ForeignKey(related_name='status', to='Mooc.CourseTime')),
            ],
        ),
        migrations.CreateModel(
            name='TestStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_counter', models.IntegerField()),
                ('unit_counter', models.IntegerField()),
                ('submit_time', models.DateTimeField(null=True, blank=True)),
                ('question_id', models.CharField(default=b'', max_length=30, blank=True)),
                ('Answer', models.CharField(default=b'', max_length=30, blank=True)),
                ('score', models.IntegerField(blank=True)),
                ('studystatus', models.ForeignKey(related_name='teststore', to='Mooc.StudyStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('gap_hour', models.IntegerField()),
                ('counter', models.IntegerField()),
                ('course', models.ForeignKey(related_name='units', to='Mooc.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UnitTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('summary', models.CharField(max_length=200)),
                ('last_time', models.DateTimeField(null=True, blank=True)),
                ('max_submit_times', models.IntegerField(default=3, blank=True)),
                ('test_content', models.OneToOneField(related_name='unit_test', blank=True, to='Mooc.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user', models.OneToOneField(related_name='info', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(unique=True, max_length=20)),
                ('school', models.CharField(max_length=20, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, choices=[(b'M', '\u7537'), (b'F', '\u5973')])),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='test',
            field=models.OneToOneField(related_name='unit', null=True, blank=True, to='Mooc.UnitTest'),
        ),
        migrations.AddField(
            model_name='studystatus',
            name='user',
            field=models.ForeignKey(related_name='status', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='unit',
            field=models.ForeignKey(related_name='sections', to='Mooc.Unit'),
        ),
        migrations.AddField(
            model_name='quizstore',
            name='studystatus',
            field=models.ForeignKey(related_name='quizstore', to='Mooc.StudyStatus'),
        ),
    ]
