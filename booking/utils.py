# coding: utf-8
from constance import config
from django.conf import settings

from .models import Booking


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

def send_mandrill_email(template, to_email=None, to_name=None, merge_vars=[], subject=False, from_email=False, from_name=False, order=False):
        try:
            import mandrill
            mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
            template_content = [{'content': '', 'name': 'tmp'}]
            message = {
                'google_analytics_domains': ['tceh.com'],
                'important': False,
                'inline_css': None,
                'merge': True,
                'merge_vars': [{'rcpt': to_email, 'vars': merge_vars}],
                'metadata': {'website': 'tceh.com'},
                'preserve_recipients': None,
                'to': [{'email': to_email, 'name': to_name, 'type': 'to'}],
                'view_content_link': None
            }
            if from_email:
                message['from_email'] = from_email

            if from_name:
                message['from_name'] = from_name

            if subject:
                message['subject'] = subject

            result = mandrill_client.messages.send_template(
                template_name=template, template_content=template_content, message=message, async=False)

            if order:
                return result
            return True
        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise


def check_mandrill_status(mandrill_id):
    try:
        import mandrill
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
        result = mandrill_client.messages.info(id=mandrill_id)
        return result

    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        return False
