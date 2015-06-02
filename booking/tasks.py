# coding: utf-8
import datetime

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import Order
from .utils import send_order_pass_mandrill


@periodic_task(run_every=(crontab(minute='*/5')))
def send_mandrill_mails_order():
    now = datetime.datetime.now()
    orders = Order.objects.filter(status=0)
    if len(orders) > 0:
        for order in orders:
            if order.date > now:
                time_diff = order.date - now
                time_diff_hours = time_diff.days * 24 + time_diff.seconds//3600
                if time_diff_hours < 1:
                    send_order_pass_mandrill(order, order.user)
