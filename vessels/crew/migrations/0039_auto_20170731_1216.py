# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-31 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0038_auto_20170731_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='incompatible_with',
            field=models.ManyToManyField(blank=True, help_text='Hold down Control, or Command on a Mac, to select more than one.', related_name='_person_incompatible_with_+', to='crew.Person'),
        ),
    ]