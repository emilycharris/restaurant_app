# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160710_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]