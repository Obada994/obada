# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 18:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Question',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='username',
            new_name='question_text',
        ),
    ]