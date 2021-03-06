# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0012_auto_20170614_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crewmanagementcompany',
            old_name='phome',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='operationsmanagementcompany',
            old_name='phome',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='safetymanagementcompany',
            old_name='phome',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='technicalmanagementcompany',
            old_name='phome',
            new_name='phone',
        ),
        migrations.AlterField(
            model_name='owner',
            name='imo_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vessels',
            name='rpm',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
