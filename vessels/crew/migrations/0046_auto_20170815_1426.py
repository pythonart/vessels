# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-15 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0045_auto_20170806_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessels',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
