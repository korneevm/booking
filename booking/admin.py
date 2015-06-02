# coding: utf-8
from django.contrib import admin

from booking.models import Booking, Order, MeetingRoom


class BookingAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'meeting_room', 'user', 'company')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'guest_fio', 'comment', 'user')


admin.site.register(MeetingRoom)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Order, OrderAdmin)
