# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-08 03:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20180207_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='due_date',
            new_name='date_due',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='time',
            new_name='time_due',
        ),
    ]
