# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 07:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_topics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='topics',
        ),
    ]
