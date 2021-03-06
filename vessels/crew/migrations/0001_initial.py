# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('date_signed_off', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salutation', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('photo', models.ImageField(upload_to='temp')),
                ('key_number', models.IntegerField(default=0)),
                ('contract', models.ManyToManyField(to='crew.Contracts')),
            ],
        ),
        migrations.CreateModel(
            name='PresentRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_promoted', models.DateField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_name', models.CharField(max_length=20)),
                ('rank_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='Vessels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('imo_no', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='presentrank',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Rank'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='contract_rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Rank'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='vessel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crew.Vessels'),
        ),
    ]
