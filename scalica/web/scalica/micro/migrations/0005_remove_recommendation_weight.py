# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 18:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro', '0004_auto_20171215_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='weight',
        ),
    ]
