from django.db import models
from assist_dids.models import *
from customers.models import *
import datetime


class Service_Order(models.Model):
    username = models.CharField(max_length=200, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    number = models.BigIntegerField(null=True, blank=True)
    texting = models.TextField(null=True, blank=True)
    requested_port_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    e911_number = models.BigIntegerField(null=True, blank=True)
    e911_address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now)