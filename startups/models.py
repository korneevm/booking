# coding: utf-8
from django.db import models
from django.utils import timezone

from users.models import User


class CompanyRole(models.Model):
    title = models.CharField(u'Название роли', max_length=100)
    title_genitive = models.CharField(u'Название роли в родительном падеже', max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Роль в компании'
        verbose_name_plural = u'Роли в компаниях'


class Startup(models.Model):
    name = models.CharField(u'Заголовок', max_length=255)
    created = models.DateTimeField(u'Дата добавления', default=timezone.now)
    members = models.ManyToManyField(User, related_name='startup_member', through='StartupMembers',
                                     verbose_name=u'Участники')

    class Meta:
        verbose_name = u'Стартап'
        verbose_name_plural = u'Стартапы'

    def __unicode__(self):
        return self.name


class StartupMembers(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Участник')
    startup = models.ForeignKey(Startup, verbose_name=u'Стартап')
    role = models.ForeignKey(CompanyRole, verbose_name=u'Роль', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = u'Участник стартапа'
        verbose_name_plural = u'Участники стартапов'
