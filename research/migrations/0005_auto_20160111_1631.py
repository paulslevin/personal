# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0004_auto_20151210_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='coauthors',
            field=models.ManyToManyField(blank=True, to='research.Coauthor'),
        ),
    ]
