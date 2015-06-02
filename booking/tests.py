# coding: utf-8
import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from users.models import User
from .models import *


class BookingTestCase(TestCase):
    def setUp(self):
        self.url = reverse('booking')
        self.client = Client()

    def _get_json(self, response):
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)

    def test_booking(self):
        today = timezone.now()
        nv = MeetingRoom.objects.create(title='nv1')
        # auth
        data = {'type': 'registration',
                'first_name': 'имя',
                'last_name': 'фамилия',
                'email': 'test2@test2.com',
                'password': 'p'}
        response = self.client.post(reverse('reg'), data)

        response = self.client.post(reverse('booking'), {'start': '8:30', 'time': '90',
                                                         'company': 'company', 'meeting_room': '1',
                                                         'cur_day': '0'})
        self.assertEqual(Booking.objects.all().count(), 1)

        response = self.client.post(reverse('booking'), {'start': '10:30', 'time': '60',
                                                         'company': 'company', 'meeting_room': '1',
                                                         'cur_day': '0'})
        self.assertEqual(Booking.objects.all().count(), 1)
        self.assertIn(u'Вы можете забронировать переговорную максимум еще на 30 минут', json.loads(response.content)['messages'])

        response = self.client.post(reverse('booking'), {'start': '10:30', 'time': '30',
                                                         'company': 'company', 'meeting_room': '1',
                                                         'cur_day': '0'})
        self.assertEqual(Booking.objects.all().count(), 2)

        response = self.client.post(reverse('booking'), {'start': '12:30', 'time': '30',
                                                         'company': 'company', 'meeting_room': '1',
                                                         'cur_day': '0'})
        self.assertEqual(Booking.objects.all().count(), 2)
        self.assertIn(u'Вы не может больше бронировать переговорную на этот день', json.loads(response.content)['messages'])

        booking2 = Booking.objects.get(id=2)
        response = self.client.post(reverse('booking'), {'type': 'remove_booking', 'booking_id': booking2.id})
        self.assertEqual(Booking.objects.all().count(), 1)
        self.assertIn(u'Бронь удалена', json.loads(response.content)['messages'])

    def test_order_pass(self):
        # auth
        data = {'type': 'registration',
                'first_name': 'имя',
                'last_name': 'фамилия',
                'email': 'andrey@andrey.com',
                'password': 'p'}
        response = self.client.post(reverse('reg'), data)

        response = self.client.post(reverse('order-pass'),
                    {'guest_fio': 'guest FIO',
                     'visit_day': '2016-12-30', 'visit_hour': '05', 'visit_minute': '40'})
        self.assertEqual(Order.objects.all().count(), 1)

        user = User.objects.latest('id')
        user.is_staff = True
        user.save()

        response = self.client.post(reverse('order-pass'),
                    {'guest_fio': 'guest FIO', 'visit_year': '2016', 'visit_month': '12',
                     'visit_day_staff': '20', 'visit_hour_staff': '20', 'visit_minute_staff': '20',
                     'comment': 'comment'})
        self.assertEqual(Order.objects.all().count(), 2)
        response = self.client.get(reverse('order-pass'))
        self.assertTrue(Order.objects.get(id=1) in response.context['orders'])

        response = self.client.post(reverse('order-pass'),
                    {'guest_fio': 'guest FIO', 'visit_year': '2016', 'visit_month': '2',
                     'visit_day_staff': '30', 'visit_hour_staff': '20', 'visit_minute_staff': '20',
                     'comment': 'comment'})
        self.assertEqual(Order.objects.all().count(), 2)
        '''
        from django.conf import settings
        import datetime
        settings.CELERY_ALWAYS_EAGER = True

        count = Order.objects.all().count()
        now = datetime.datetime.now()

        for i in range(1, 1000):
            response = self.client.post(reverse('order-pass'),
                    {'guest_fio': 'guest NOW', 'visit_year': str(now.year), 'visit_month': str(now.month),
                     'visit_day_staff': str(now.day), 'visit_hour_staff': str(now.hour + 1), 'visit_minute_staff': str(0),
                     'comment': 'comment', 'test': 'test'})
            self.assertEqual(Order.objects.all().count(), count + i)
            order = Order.objects.latest('id')
            self.assertTrue(order.status, 'sent')
            print order

        count = Order.objects.all().count()
        for i in range(1, 1000):
            response = self.client.post(reverse('order-pass'),
                    {'guest_fio': 'guest FUTURE', 'visit_year': str(now.year), 'visit_month': str(now.month),
                     'visit_day_staff': str(now.day), 'visit_hour_staff': str(now.hour + 2), 'visit_minute_staff': str(0),
                     'comment': 'comment', 'test': 'test'})
            self.assertEqual(Order.objects.all().count(), count + i)
            order = Order.objects.latest('id')
            self.assertTrue(order.status, 'sent')
            print order
        '''