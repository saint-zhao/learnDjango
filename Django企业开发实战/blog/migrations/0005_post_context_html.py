# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-05-02 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190426_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='context_html',
            field=models.TextField(blank=True, editable=False, verbose_name='正文html代码'),
        ),
    ]
