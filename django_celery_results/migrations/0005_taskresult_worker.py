# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-24 15:38

# this file is auto-generated so don't do flake8 on it
# flake8: noqa

from __future__ import absolute_import, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celery_results', '0004_auto_20190516_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskresult',
            name='worker',
            field=models.CharField(db_index=True, default=None,
                                   help_text='Worker that executes the task',
                                   max_length=100, null=True,
                                   verbose_name='Worker'),
        ),
    ]
