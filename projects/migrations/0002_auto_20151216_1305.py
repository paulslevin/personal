# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polynomial',
            name='poynomial',
            field=models.CharField(max_length=500, verbose_name='polynomial'),
        ),
    ]
