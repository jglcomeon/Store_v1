# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-22 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alipay', '0002_auto_20200322_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]