# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-17 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0023_auto_20180211_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='submitted_files/')),
                ('date_submitted', models.DateField(blank=True)),
                ('time_submitted', models.TimeField(blank=True)),
                ('correct', models.BooleanField(default=False)),
                ('comment_ratio', models.IntegerField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Assignment')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserProfile')),
            ],
        ),
    ]