# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0014_auto_20170614_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='department_type',
            field=models.CharField(max_length=200),
        ),
    ]
