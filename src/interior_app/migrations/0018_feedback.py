# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-18 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interior_app', '0017_remove_subscriber_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos')),
            ],
        ),
    ]
