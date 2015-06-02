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
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=255, verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u044f \u0431\u0440\u043e\u043d\u0438')),
                ('start', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430')),
                ('end', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u0430\u044f',
                'verbose_name_plural': '\u0417\u0430\u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u044b\u0435',
            },
        ),
        migrations.CreateModel(
            name='MeetingRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u043e\u0439')),
            ],
            options={
                'verbose_name': '\u041f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u0430\u044f',
                'verbose_name_plural': '\u041f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u044b\u0435',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u044f \u043f\u0440\u043e\u043f\u0443\u0441\u043a\u0430')),
                ('guest_fio', models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f \u0418\u043c\u044f \u0433\u043e\u0441\u0442\u044f (\u0435\u0441\u043b\u0438 \u0433\u043e\u0441\u0442\u0435\u0439 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e - \u0447\u0435\u0440\u0435\u0437 \u0437\u0430\u043f\u044f\u0442\u0443\u044e)')),
                ('comment', models.TextField(verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 (\u043a \u043a\u043e\u043c\u0443 \u0438\u043c\u0435\u043d\u043d\u043e \u0438\u0434\u0435\u0442 \u0433\u043e\u0441\u0442\u044c? \u044d\u0442\u0430 \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043d\u0435 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043d\u0430 \u043e\u0445\u0440\u0430\u043d\u0443)')),
                ('date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u0432\u0438\u0437\u0438\u0442\u0430')),
                ('status', models.CharField(blank=True, max_length=25, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(0, '\u0411\u0443\u0434\u0435\u0442 \u0437\u0430\u043a\u0430\u0437\u0430\u043d'), (1, '\u0412 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0435, \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443 \u0447\u0435\u0440\u0435\u0437 \u043c\u0438\u043d\u0443\u0442\u0443'), (2, '\u041f\u0440\u043e\u043f\u0443\u0441\u043a \u0437\u0430\u043a\u0430\u0437\u0430\u043d')])),
                ('message_id', models.CharField(max_length=255, null=True, verbose_name='ID mandrill', blank=True)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u043f\u0443\u0441\u043a',
                'verbose_name_plural': '\u041f\u0440\u043e\u043f\u0443\u0441\u043a\u0430',
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='meeting_room',
            field=models.ForeignKey(verbose_name='\u041f\u0435\u0440\u0435\u0433\u043e\u0432\u043e\u0440\u043d\u0430\u044f', to='booking.MeetingRoom'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
    ]
