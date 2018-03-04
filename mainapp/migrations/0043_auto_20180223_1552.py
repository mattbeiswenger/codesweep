# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-23 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0042_courselist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courselist',
            name='course',
            field=models.CharField(choices=[('CSC', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior')], max_length=128),
        ),
    ]