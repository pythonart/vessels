# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-31 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0040_auto_20170731_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewcertificatelist',
            name='required_for_ranks',
            field=models.ManyToManyField(help_text='Hold down Control, or Command on a Mac, to select more than one.', to='crew.Rank'),
        ),
    ]
