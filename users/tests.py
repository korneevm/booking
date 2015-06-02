# coding: utf-8
import os
import datetime

from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory, Client
from django.template import RequestContext, Template, Context
from django.http import HttpRequest

from users.models import User

