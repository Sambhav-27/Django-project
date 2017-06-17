# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_finalbuy'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalbuy',
            name='buy_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date bought'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='finalbuy',
            name='tranno',
            field=models.IntegerField(default=0),
        ),
    ]
