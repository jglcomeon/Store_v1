# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-07 07:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsinfo',
            options={'ordering': ['gclick']},
        ),
    ]