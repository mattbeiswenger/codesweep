# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-26 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='inputs',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]