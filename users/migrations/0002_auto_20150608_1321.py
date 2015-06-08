# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='startup_name',
            field=models.CharField(max_length=250, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0430\u0440\u0442\u0430\u043f\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='permission_granted',
            field=models.BooleanField(default=False, help_text='\u041e\u0442\u043c\u0435\u0442\u044c\u0442\u0435, \u0435\u0441\u043b\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0434\u043e\u043b\u0436\u0435\u043d \u0438\u043c\u0435\u0442\u044c \u0432\u043e\u0437\u043c\u043e\u0436\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u043f\u0440\u043e\u043f\u0443\u0441\u043a\u0430 \u0438 \u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u044b\u0435 \u043a\u043e\u043c\u043d\u0430\u0442\u044b', verbose_name='\u0414\u043e\u0441\u0442\u0443\u043f \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043d'),
        ),
    ]
