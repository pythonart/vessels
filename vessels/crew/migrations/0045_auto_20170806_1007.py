# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-06 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0044_auto_20170802_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='generalSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_year_start', models.DateField(help_text='Date financial year starts yyy-mm-dd')),
                ('financial_year_ends', models.DateField(help_text='Date financial year ends yyy-mm-dd')),
            ],
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_expired',
            field=models.DateField(help_text='yyy-mm-dd', verbose_name='Date Contract Ends'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_started',
            field=models.DateField(help_text='yyy-mm-dd', verbose_name='Date Contract Started'),
        ),
        migrations.AlterField(
            model_name='crewcertificates',
            name='date_expiry',
            field=models.DateField(blank=True, help_text='yyy-mm-dd', null=True),
        ),
        migrations.AlterField(
            model_name='crewcertificates',
            name='date_issued',
            field=models.DateField(help_text='yyy-mm-dd'),
        ),
        migrations.AlterField(
            model_name='crewmanagementcompany',
            name='department_type',
            field=models.ManyToManyField(help_text='Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple', to='crew.Departments'),
        ),
        migrations.AlterField(
            model_name='operationsmanagementcompany',
            name='department_type',
            field=models.ManyToManyField(help_text='Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple', to='crew.Departments'),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_joined_company',
            field=models.DateField(blank=True, help_text='yyy-mm-dd', null=True, verbose_name='Date Join Organisation'),
        ),
        migrations.AlterField(
            model_name='person',
            name='dob',
            field=models.DateField(help_text='yyy-mm-dd', verbose_name='Date Of Birth'),
        ),
        migrations.AlterField(
            model_name='safetymanagementcompany',
            name='department_type',
            field=models.ManyToManyField(help_text='Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple', to='crew.Departments'),
        ),
        migrations.AlterField(
            model_name='seatime',
            name='date_signed_off',
            field=models.DateField(blank=True, help_text='yyy-mm-dd', null=True, verbose_name='Date Signed Off'),
        ),
        migrations.AlterField(
            model_name='seatime',
            name='date_signed_on',
            field=models.DateField(help_text='yyy-mm-dd', verbose_name='Date Signed On'),
        ),
        migrations.AlterField(
            model_name='technicalmanagementcompany',
            name='department_type',
            field=models.ManyToManyField(help_text='Select Departments That Fall Under This Company. Hold Control or Command on Mac for Multiple', to='crew.Departments'),
        ),
    ]
