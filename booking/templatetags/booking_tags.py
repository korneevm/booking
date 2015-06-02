import datetime

from django import template


register = template.Library()


@register.filter
def get_time_for_status(date):
    return date - datetime.timedelta(hours=1)
