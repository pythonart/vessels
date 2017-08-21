# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 12:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0007_auto_20170610_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentrank',
            name='person',
        ),
        migrations.AddField(
            model_name='person',
            name='rank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crew.PresentRank'),
            preserve_default=False,
        ),
    ]
