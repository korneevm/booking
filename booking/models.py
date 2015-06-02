# coding: utf-8
from django.db import models
from django.utils import timezone

from model_utils import Choices

from users.models import User


class MeetingRoom(models.Model):
    title = models.CharField(u'Название переговорной', max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Переговорная'
        verbose_name_plural = u'Переговорные'


class Booking(models.Model):
    company = models.CharField(u'Компания', max_length=255)
    created = models.DateTimeField(u'Дата и время оформления брони', default=timezone.now)
    meeting_room = models.ForeignKey(MeetingRoom, verbose_name=u'Переговорная')
    start = models.DateTimeField(u'Дата и время начала')
    end = models.DateTimeField(u'Дата и время окончания')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')

    class Meta:
        verbose_name = u'Забронированная переговорная'
        verbose_name_plural = u'Забронированные переговорные'

    def __unicode__(self):
        return '%s - %s %s' % (self.start, self.end, self.user.get_full_name())


class Order(models.Model):
    STATUS_TYPES = Choices(
        (0, u'Будет заказан'),
        (1, u'В обработке, обновите страницу через минуту'),
        (2, u'Пропуск заказан'),
    )
    created = models.DateTimeField(u'Дата и время оформления пропуска', default=timezone.now)
    guest_fio = models.CharField(u'Фамилия Имя гостя (если гостей несколько - через запятую)', max_length=255)
    comment = models.TextField(u'Комментарий (к кому именно идет гость? эта информация не отправляется на охрану)')
    date = models.DateTimeField(u'Дата и время визита')
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    status = models.CharField(u'Статус', choices=STATUS_TYPES, max_length=25, null=True, blank=True)
    message_id = models.CharField(u'ID mandrill', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u'Пропуск'
        verbose_name_plural = u'Пропуска'

    def __unicode__(self):
        return '%s: %s' % (self.date, self.guest_fio)

    @property
    def display_status(self):
        return self.STATUS_TYPES[int(self.status)]
