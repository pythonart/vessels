# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-04 11:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0029_auto_20170703_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='rank_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Departments'),
        ),
    ]
