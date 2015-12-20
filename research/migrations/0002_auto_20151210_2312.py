# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='address',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coauthor',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='coauthor',
            name='coauthor',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='coauthor',
            name='institution',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='paper',
            name='publish_date',
            field=models.DateField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
