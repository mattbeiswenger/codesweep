# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-08 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20180207_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='function_name',
            field=models.CharField(blank=True, default='function', max_length=128),
        ),
    ]