# coding: utf-8
import calendar
from datetime import datetime, date, timedelta

from pytils import dt
import floppyforms as forms
from constance import config


def get_months():
    months = []
    for i in range(1, 13):
        months.append((i, i))
    return months


def get_years():
    years = []
    today = date.today()
    for v in range(today.year, today.year + 5):
        years.append((v, v))
    return years


def get_days_staff():
    days = []
    for i in range(1, 32):
        days.append((i, i))
    return days


def get_days():
    days = []
    today = date.today()
    days.append((str(today), dt.ru_strftime(u"%d %B", today, inflected=True)))
    for i in range(1, int(config.ORDERS_DAYS)):
        try:
            next_day = date(today.year, today.month, today.day + timedelta(days=i).days)
        except ValueError:
            _, monthdays = calendar.monthrange(today.year, today.month)
            day = today.day + timedelta(days=i).days
            if monthdays < day:
                surplus = day - monthdays
                next_day = date(today.year, today.month, monthdays) + timedelta(days=surplus)
        days.append((str(next_day), dt.ru_strftime(u"%d %B", next_day, inflected=True)))
    return days


def get_hours():
    hours = []
    for i in range(0, 24):
        hours.append((i, "%02d" % i))
    return hours


def get_minutes():
    minutes = []
    for i in range(0, 60):
        if i % 10 == 0:
            minutes.append((i, "%02d" % i))
    return minutes


def get_initial_day():
    d = str(date.today())
    return d


def get_initial_hour():
    h = datetime.now().hour
    return h


def get_initial_minutes():
    import math
    m = datetime.now().minute
    m = int(math.ceil((m + 10) / 10) * 10)
    if m == 60:
        m = 0
    return m


class BookingForm(forms.Form):
    time = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'field-dropdown-input time', 'placeholder': u'Сколько минут', 'readonly': 'readonly'},
    ))


class OrderForm(forms.Form):
    guest_fio = forms.CharField(label=u'Фамилия и Имя гостя',
                                help_text=u'Если гостей несколько, введите их данные через запятую',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'required': 'required'},
                                    ))
    visit_day = forms.CharField(label=u'День', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required', 'data-day': get_initial_day()}, choices=get_days()
    ), required=True)
    visit_hour = forms.CharField(label=u'Часы', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_hours()
    ), required=True)
    visit_minute = forms.CharField(label=u'Минуты', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_minutes()
    ), required=True)

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        visit_day = cleaned_data.get("visit_day")
        hours = cleaned_data.get("visit_hour")
        minute = cleaned_data.get("visit_minute")
        try:
            visit_date = visit_day.split('-')
            visit_date = datetime(int(visit_date[0]), int(visit_date[1]), int(visit_date[2]), int(hours), int(minute))
        except Exception, e:
            raise forms.ValidationError(u"Введите правильную дату")

        if datetime.now() > visit_date:
            raise forms.ValidationError(u"Вы не можете заказывать пропуск в прошлое")

        return cleaned_data


class OrderAdminForm(forms.Form):
    guest_fio = forms.CharField(label=u'Фамилия и Имя гостя',
                                help_text=u'Если гостей несколько, введите их данные через запятую',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'required': 'required'},
                                    ))
    visit_year = forms.CharField(label=u'Год', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_years()
    ), required=True)
    visit_month = forms.CharField(label=u'Месяц', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_months()
    ), required=True)
    visit_day_staff = forms.CharField(label=u'День', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_days_staff()
    ), required=True)

    visit_hour_staff = forms.CharField(label=u'Часы', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_hours()
    ), required=True)
    visit_minute_staff = forms.CharField(label=u'Минуты', widget=forms.Select(
        attrs={'class': 'form-control', 'required': 'required'}, choices=get_minutes()
    ), required=True)

    comment = forms.CharField(label=u'К кому идет гость?', help_text=u'Эта информация не отправляется на охрану',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'required': 'required'}
                              ))

    def clean(self):
        cleaned_data = super(OrderAdminForm, self).clean()
        year = cleaned_data.get("visit_year")
        month = cleaned_data.get("visit_month")
        day = cleaned_data.get("visit_day_staff")
        hours = cleaned_data.get("visit_hour_staff")
        minute = cleaned_data.get("visit_minute_staff")
        try:
            visit_date = datetime(int(year), int(month), int(day), int(hours), int(minute))
        except Exception, e:
            raise forms.ValidationError(u"Введите правильную дату")

        if datetime.now() > visit_date:
            raise forms.ValidationError(u"Вы не можете заказывать пропуск в прошлое")

        return cleaned_data