# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u043e\u043b\u0438')),
                ('title_genitive', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u043e\u043b\u0438 \u0432 \u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u043c \u043f\u0430\u0434\u0435\u0436\u0435')),
            ],
            options={
                'verbose_name': '\u0420\u043e\u043b\u044c \u0432 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438',
                'verbose_name_plural': '\u0420\u043e\u043b\u0438 \u0432 \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f\u0445',
            },
        ),
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u0440\u0442\u0430\u043f',
                'verbose_name_plural': '\u0421\u0442\u0430\u0440\u0442\u0430\u043f\u044b',
            },
        ),
        migrations.CreateModel(
            name='StartupMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(verbose_name='\u0420\u043e\u043b\u044c', blank=True, to='startups.CompanyRole', null=True)),
                ('startup', models.ForeignKey(verbose_name='\u0421\u0442\u0430\u0440\u0442\u0430\u043f', to='startups.Startup')),
                ('user', models.ForeignKey(verbose_name='\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a \u0441\u0442\u0430\u0440\u0442\u0430\u043f\u0430',
                'verbose_name_plural': '\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0438 \u0441\u0442\u0430\u0440\u0442\u0430\u043f\u043e\u0432',
            },
        ),
        migrations.AddField(
            model_name='startup',
            name='members',
            field=models.ManyToManyField(related_name='startup_member', verbose_name='\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0438', through='startups.StartupMembers', to=settings.AUTH_USER_MODEL),
        ),
    ]
