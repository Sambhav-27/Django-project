# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 04:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
