from django.db import models
from django.utils.translation import gettext_lazy as _
from assist_dids.models import *
from customers.models import *
import datetime

class StatusValues(models.IntegerChoices):
    CREATED = 0, _('Created')
    UPDATED = 1, _('Updated')
    DELETED = 2, _('Deleted')

class SwitchValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')

class Service_Order(models.Model):
    username = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=255, unique=True, null=True, blank=True)
    texting = models.TextField(null=True, blank=True)
    requested_port_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    e911_number = models.BigIntegerField(null=True, blank=True)
    e911_address = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_service_order', to_field='record_id')
    reseller = models.CharField(max_length=200, null=True, blank=True)
    status = models.BigIntegerField(default=0, null=False, blank=False)
    service_status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    voice_carrier = models.ForeignKey(Voice_Carrier, on_delete=models.CASCADE, null=True, blank=True, related_name='voice_carrier_service_order', to_field='record_id')
    sms_carrier = models.ForeignKey(Voice_Carrier, on_delete=models.CASCADE, null=True, blank=True, related_name='sms_carrier_service_order', to_field='record_id')
    sms_type = models.ForeignKey(SMS_Type, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    term_location = models.ForeignKey(Term_Location, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    sms_enabled = models.CharField(max_length=3, choices=SwitchValues.choices, null=True, blank=True)
    sms_campaign = models.CharField(max_length=100, null=True, blank=True)
    user_first_name = models.CharField(max_length=100, null=True, blank=True)
    user_last_name = models.CharField(max_length=100, null=True, blank=True)
    extension = models.BigIntegerField(null=True, blank=True)
    onboard_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=3, choices=SwitchValues.choices, null=True, blank=True)
    service_1 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_order_1', blank=True, to_field='record_id')
    service_2 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_order_2', blank=True, to_field='record_id')
    service_3 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_order_3', blank=True, to_field='record_id')
    service_4 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name='service_order_4', blank=True, to_field='record_id')
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now)