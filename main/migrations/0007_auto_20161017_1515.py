# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-17 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20161017_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateField(),
        ),
    ]
