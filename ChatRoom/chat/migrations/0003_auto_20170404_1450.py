# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 18:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20170404_1330'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chatroommembership',
            unique_together=set([('user', 'chat_room')]),
        ),
    ]