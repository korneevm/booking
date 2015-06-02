from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from booking.views import BookingIndexView, BookingView, OrderPass

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^booking/$', login_required(BookingView.as_view()), name='booking'),
    url(r'^order-pass/$', login_required(OrderPass.as_view()), name='order-pass'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', BookingIndexView.as_view()),
]
