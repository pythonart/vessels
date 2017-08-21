# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-31 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0041_auto_20170731_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='incompatible_with',
            field=models.ManyToManyField(blank=True, help_text='<p class="help">Hold down Control, or Command on a Mac, \n                                                to select more than one. Hold down "Control", or "Command" on a Mac, to select more than one.</p>', related_name='_person_incompatible_with_+', to='crew.Person'),
        ),
    ]