# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-18 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0022_auto_20170618_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='rank_name',
            field=models.CharField(max_length=100),
        ),
    ]