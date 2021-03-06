# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-11 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gtitle', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to='goods')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idDelete', models.BooleanField(default=False)),
                ('gunit', models.CharField(default='500g', max_length=20)),
                ('gclick', models.IntegerField()),
                ('gjianjie', models.CharField(max_length=200)),
                ('gkucun', models.IntegerField()),
                ('gcontent', tinymce.models.HTMLField()),
            ],
            options={
                'ordering': ['-gclick'],
            },
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.TypeInfo'),
        ),
    ]
