# coding: utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import user_signed_up
from constance import config

from .utils import send_mandrill_email


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(u'Имя', max_length=150, null=True, blank=True)
    last_name = models.CharField(u'Фамилия', max_length=150, null=True, blank=True)
    email = models.EmailField(u'E-mail', unique=True, blank=True)

    startup_name = models.CharField(u'Название стартапа', max_length=250, null=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    permission_granted = models.BooleanField(u'Доступ разрешен', default=False,
                                             help_text=u'Отметьте, если пользователь должен иметь '
                                                       u'возможность заказывать пропуска и бронировать '
                                                       u'переговорные комнаты')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def __unicode__(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        elif self.email:
            return self.email
        else:
            return self.pk

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.first_name:
            if len(self.first_name) > 0:
                if self.first_name[0] == ' ':
                    self.first_name = self.first_name[1:]
            if len(self.first_name) > 0:
                if self.first_name[-1] == ' ':
                    self.first_name = self.first_name[:-1]
        if self.last_name:
            if len(self.last_name) > 0:
                if self.last_name[0] == ' ':
                    self.last_name = self.last_name[1:]
            if len(self.last_name) > 0:
                if self.last_name[-1] == ' ':
                    self.last_name = self.last_name[:-1]
        super(User, self).save(using=using, force_insert=force_insert,
                               force_update=force_update, update_fields=update_fields)

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name or self.email

    def can_book_meeting_room(self):
        return self.permission_granted or self.is_staff

    def can_order_pass(self):
        return self.permission_granted or self.is_staff


@receiver(user_signed_up)
def user_signed_up_(request, **kwargs):
    user = kwargs.pop('user')
    data = [
        {'name': u'user_email', 'content': user.email},
        {'name': u'user_first_name', 'content': user.first_name},
        {'name': u'user_last_name', 'content': user.last_name},
        {'name': u'startup_name', 'content': user.startup_name},
        ]
    result = send_mandrill_email('new-user-signin', config.ORDERS_ADMIN_EMAIL, '', data)
    return result