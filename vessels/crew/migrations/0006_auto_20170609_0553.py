# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 05:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0005_auto_20170609_0547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='contract',
        ),
        migrations.AddField(
            model_name='contracts',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crew.Person'),
            preserve_default=False,
        ),
    ]
