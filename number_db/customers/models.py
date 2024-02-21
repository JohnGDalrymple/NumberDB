from django.db import models
import datetime
from assist_dids.models import *

# Create your models here.

class Customer(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    billing_address = models.CharField(max_length=200, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)
    billing_state = models.CharField(max_length=20, null=True, blank=True)
    billing_zipcode = models.CharField(max_length=20, null=True, blank=True)
    billing_country = models.CharField(max_length=50, null=True, blank=True)
    e911_address = models.CharField(max_length=200, null=True, blank=True)
    e911_city = models.CharField(max_length=100, null=True, blank=True)
    e911_state = models.CharField(max_length=20, null=True, blank=True)
    e911_zipcode = models.CharField(max_length=20, null=True, blank=True)
    e911_country = models.CharField(max_length=50, null=True, blank=True)
    customer_type = models.ForeignKey(Customer_Type, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_type', to_field='record_id')
    support_contract = models.CharField(max_length=200, null=True, blank=True)
    attachments = models.BigIntegerField(null=True, blank=True)
    open_balance = models.FloatField(null=True, blank=True)
    record_id = models.BigIntegerField(null=True, blank=True, unique=True)
    note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now)