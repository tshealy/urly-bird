# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('time', models.DateTimeField(null=True, default=django.utils.timezone.now)),
                ('address', models.CharField(null=True, max_length=500)),
                ('browser', models.CharField(null=True, max_length=500)),
                ('user', models.IntegerField(null=True, max_length=255)),
                ('bookmark', models.ForeignKey(to='bookmark.Bookmark')),
            ],
        ),
    ]
