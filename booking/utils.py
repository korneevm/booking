# coding: utf-8
from constance import config
from django.conf import settings

from .models import Booking
from users.utils import send_mandrill_email


def can_book(day, company):

    bookings_today = Booking.objects.filter(company=company, start__year=day.year, start__month=day.month,
                                            start__day=day.day)
    booked_time = sum([(b.end - b.start).seconds / float(60 * 60) for b in bookings_today])

    booked_time = booked_time
    if booked_time >= config.BOOKING_HOURS:
        return False
    return (config.BOOKING_HOURS - booked_time) * 60


def send_order_pass_mandrill(order, user):
    data = [{'name': u'guest_fio', 'content': order.guest_fio},
            {'name': u'date', 'content': order.date.strftime("%d.%m.%Y %H:%M")},
            {'name': u'comment', 'content': order.comment},
            {'name': u'user_email', 'content': user.email},
            {'name': u'user_first_name', 'content': user.first_name},
            {'name': u'user_last_name', 'content': user.last_name},
            ]

    result = send_mandrill_email('order-coworking-pass', config.ORDERS_EMAIL, '', data, order=True)

    message_status = result[0].get('status')
    order.message_id = result[0].get('_id')

    if message_status == 'sent':
        order.status = 2
    elif message_status == 'rejected':
        order.status = 0
    else:
        order.status = 1
    order.save()