# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0027_auto_20170703_2033'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seatime',
            unique_together=set([('date_signed_off', 'person'), ('date_signed_on', 'date_signed_off', 'person'), ('date_signed_on', 'person')]),
        ),
    ]
