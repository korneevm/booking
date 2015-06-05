# coding: utf-8
import datetime
import json
import pytils
from collections import defaultdict

from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from constance import config

from users.models import User
from startups.models import Startup

from .forms import BookingForm, OrderForm, OrderAdminForm, get_months, get_days, get_days_staff,\
    get_hours, get_initial_hour, get_initial_minutes, get_minutes, get_years, get_initial_day
from .models import Booking, MeetingRoom, Order
from .utils import can_book, send_order_pass_mandrill, check_mandrill_status


class BookingIndexView(View):

    def get(self, request):
        return HttpResponseRedirect(reverse('order-pass'))


class BookingView(TemplateView):
    template_name = 'pages/booking.html'

    @staticmethod
    def ajax_render_to_response(context, **response_kwargs):
        return HttpResponse(
            json.dumps(context),
            content_type='application/json',
            **response_kwargs
        )

    def show_messages(self, booking=None):
        html = render_to_string('registration/reg_messages.html', {'messages': messages.get_messages(self.request)})
        data = {'messages': html}
        if booking:
            data['booking_company'] = booking.company
            data['booking_user'] = booking.user.get_full_name()
            data['booking_id'] = booking.id
            data['addevent_data'] = {'summary': u'Бронь переговорной "%s"' % booking.meeting_room.title,
                                     'start': booking.start.strftime("%m-%d-%Y %H:%M:%S"),
                                     'end': booking.end.strftime("%m-%d-%Y %H:%M:%S"),
                                     'description': u'Бронь переговорной "%s"' % booking.meeting_room.title,
                                     'location': u'Москва, Серебрянническая наб., 29, 7-й этаж, переговорная "%s"' % booking.meeting_room.title}
        return self.ajax_render_to_response(data)

    def calendar_day(self, day):
        today = timezone.now()
        cur_day = today + datetime.timedelta(days=day)

        prev = cur_day - datetime.timedelta(days=1)
        prev_day = pytils.dt.ru_strftime(u"%d %B", prev, inflected=True)

        next = cur_day + datetime.timedelta(days=1)
        next_day = pytils.dt.ru_strftime(u"%d %B", next, inflected=True)

        today_min = datetime.datetime.combine(cur_day, datetime.time.min)
        today_max = datetime.datetime.combine(cur_day, datetime.time.max)
        bookings = Booking.objects.filter(start__range=(today_min, today_max))
        cur_data = {}

        for booking in bookings:
            owner = 'own' if booking.user == self.request.user else 'alien'
            start = str(booking.start.hour) + ':' + str(booking.start.minute)
            duration = (booking.end - booking.start).seconds / 60

            if owner == 'own':
                if booking.company:
                    company = booking.company
                else:
                    company = u'Забронировано вами'
            elif booking.user.is_staff and booking.company == booking.user.get_full_name():
                company = 'Акселератор'
            else:
                company = booking.company

            creator = booking.user.get_full_name()

            cur_data[str(booking.id)] = {'company': company, 'start': start, 'duration': duration, 'creator': creator,
                                         'owner': owner, 'nv': str(booking.meeting_room.id),
                                         'addevent_data': {
                                             'summary': u'Бронь переговорной "%s"' % booking.meeting_room.title,
                                             'start': booking.start.strftime("%m-%d-%Y %H:%M:%S"),
                                             'end': booking.end.strftime("%m-%d-%Y %H:%M:%S"),
                                             'description': u'Бронь переговорной "%s"' % booking.meeting_room.title,
                                             'location': u'Москва, Серебрянническая наб., 29, 7-й этаж, '
                                                         u'переговорная "%s"' % booking.meeting_room.title
                                         }
            }
        is_staff = self.request.user.is_staff
        data = {'next': {'id': day + 1, 'day': next_day}, 'prev': {'id': day - 1, 'day': prev_day}, 'is_staff': is_staff,
                'cur_id': day, 'cur': pytils.dt.ru_strftime(u"%d %B, %A", cur_day, inflected=True), 'cur_data': cur_data
                }
        return data

    def get_context_data(self, **kwargs):
        context = super(BookingView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            days_count = 10000
        else:
            days_count = config.PROFILE_BOOKING_CALENDAR_DAYS
        form = BookingForm()
        nv = MeetingRoom.objects.all()
        startups = Startup.objects.all()
        hours = ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                 '16:00', '17:00', '18:00', '19:00', '20:00']

        return {'form': form, 'nv': nv, 'hours': hours, 'days_count': days_count, 'startups': startups}

    def get(self, request, *args, **kwargs):
        if request.is_ajax and request.GET.get('day_id'):
            calendar_day = self.calendar_day(int(request.GET.get('day_id')))
            return self.ajax_render_to_response({'calendar_day': calendar_day})
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        start = request.POST.get('start')
        time = request.POST.get('time')
        startup = request.POST.get('startup')
        meeting_room_id = request.POST.get('meeting_room')
        cur_day = request.POST.get('cur_day')

        booking_id = request.POST.get('booking_id')
        booking_type = request.POST.get('type')
        if booking_type and booking_type == 'remove_booking' and booking_id:
            try:
                booking = Booking.objects.get(id=int(booking_id))
                if request.user.is_staff or request.user == booking.user:
                    booking.delete()
                    messages.info(request, u'Бронь удалена', extra_tags='notification')
                    return self.show_messages()
                else:
                    messages.error(request, u'Вам отказано в доступе к операции', extra_tags='notification')
                    return self.show_messages()
            except Booking.DoesNotExist:
                messages.info(request, u'Данной брони уже не существует. Обновите страницу.', extra_tags='notification')
                return self.show_messages()

        nv = MeetingRoom.objects.get(id=int(meeting_room_id))

        today = datetime.datetime.today() + datetime.timedelta(days=int(cur_day))
        s = start.split(':')
        start = datetime.datetime(today.year, today.month, today.day, int(s[0]), int(s[1]))
        # set min time if time data was bugged
        if time:
            t = int(time.split(' ')[0])
        else:
            t = 30
        end = start + datetime.timedelta(minutes=t)

        already_booked = Booking.objects.filter(Q(start__gt=start, start__lt=end, meeting_room=nv)
                                                | Q(end__gt=start, end__lt=end, meeting_room=nv)).count()
        if already_booked > 0:
            messages.warning(request, u'На это время уже оформлен заказ', extra_tags='notification')
            return self.show_messages()

        if startup:
            company = startup
        else:
            av_time = True
            available_time = 120
            startups = Startup.objects.filter(members__id__exact=request.user.id)
            if len(startups):
                startup = startups[0]
                company = startup.name
                if not request.user.is_staff:
                    available_time = can_book(today, company)
                    if not available_time:
                        av_time = None

            else:
                company = request.user.get_full_name()
                if not request.user.is_staff:
                    available_time = can_book(today, company)
                    if not available_time:
                        av_time = None

            if not av_time:
                messages.warning(request, u'Вы не может больше бронировать переговорную на этот день',
                                 extra_tags='notification')
                return self.show_messages()

            if available_time < t:
                messages.warning(request, u'Вы можете забронировать переговорную максимум '
                                          u'еще на %s минут на этот день' % int(available_time),
                                 extra_tags='notification')
                return self.show_messages()

        booking, created = Booking.objects.get_or_create(start=start, end=end, company=company,
                                                         meeting_room=nv, user=request.user)
        messages.info(request, u'Бронь заказана', extra_tags='notification')
        return self.show_messages(booking)


class OrderPass(TemplateView):
    template_name = 'pages/order_pass.html'

    def get_orders(self):
        user = self.request.user
        if user.is_staff:
            users = User.objects.filter(is_staff=True)
            orders = []
            for user in users:
                orders.extend(Order.objects.filter(user=user))
            orders.sort(key=lambda x: x.date, reverse=True)
        else:
            startups = Startup.objects.filter(members__id__exact=self.request.user.id)
            if len(startups):
                startup = startups[0]
                users = startup.members.all()
                orders = []
                for user in users:
                    orders.extend(Order.objects.filter(user=user))
                orders.sort(key=lambda x: x.date, reverse=True)
            else:
                orders = Order.objects.filter(user=self.request.user).order_by('-date')

        for mail in orders:
            if mail.message_id and mail.status == 1:
                result = check_mandrill_status(mail.message_id)
                if result:
                    if result.get('state') == 'sent':
                        mail.status = 2
                        mail.save()

        groups = defaultdict(list)
        for obj in orders:
            groups[obj.date.date()].append(obj)
        orders = groups.values()
        orders.sort(key=lambda x: x[0].date, reverse=True)
        return orders

    def get_form(self, post=None):
        initial = {}
        if self.request.user.is_authenticated and self.request.user.is_staff:
            if post:
                form = OrderAdminForm
            else:
                initial['visit_month'] = datetime.datetime.now().month
                initial['visit_day_staff'] = datetime.datetime.now().day
                initial['visit_hour_staff'] = get_initial_hour()
                initial['visit_minute_staff'] = get_initial_minutes()
                form = OrderAdminForm(initial=initial)
        else:
            if post:
                form = OrderForm
            else:
                initial['visit_hour'] = get_initial_hour()
                initial['visit_minute'] = get_initial_minutes()
                initial['visit_day'] = get_initial_day()
                form = OrderForm(initial=initial)
        if post:
            return form(post)
        return form

    def get_context_data(self, **kwargs):
        context = super(OrderPass, self).get_context_data(**kwargs)
        form = self.get_form()
        orders_group = self.get_orders()

        paginator = Paginator(orders_group, 7)
        page = self.request.GET.get('page')

        try:
            orders_group = paginator.page(page)
        except PageNotAnInteger:
            orders_group = paginator.page(1)
        except EmptyPage:
            orders_group = paginator.page(paginator.num_pages)

        orders = [item for sublist in orders_group for item in sublist]

        return {'orders': orders, 'form': form, 'paginator': paginator, 'orders_group': orders_group}

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST)
        if form.is_valid():
            guest_fio = form.cleaned_data.get('guest_fio')

            visit_day = form.cleaned_data.get("visit_day")
            hours = form.cleaned_data.get("visit_hour")
            minute = form.cleaned_data.get("visit_minute")

            visit_year = form.cleaned_data.get("visit_year")
            visit_month = form.cleaned_data.get("visit_month")
            visit_day_staff = form.cleaned_data.get("visit_day_staff")
            hours_staff = form.cleaned_data.get("visit_hour_staff")
            minute_staff = form.cleaned_data.get("visit_minute_staff")
            comment = form.cleaned_data.get('comment', '')

            user = request.user
            if user.is_staff:
                date = datetime.datetime(int(visit_year), int(visit_month), int(visit_day_staff),
                                         int(hours_staff), int(minute_staff))
            else:
                visit_date = visit_day.split('-')
                date = datetime.datetime(int(visit_date[0]), int(visit_date[1]), int(visit_date[2]),
                                         int(hours), int(minute))

            order, created = Order.objects.get_or_create(guest_fio=guest_fio, date=date,
                                                         user=user, comment=comment)
            if created:
                now = datetime.datetime.now()
                if now + datetime.timedelta(hours=1) < date:
                    order.status = 0
                    order.save(update_fields=['status'])
                else:
                    send_order_pass_mandrill(order, user)

            return HttpResponseRedirect(reverse('order-pass'))
        else:
            return render_to_response('pages/order_pass.html', {'form': form}, context_instance=RequestContext(request))
