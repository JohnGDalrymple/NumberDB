from django.db import models
from django.utils.translation import gettext_lazy as _
from assist_dids.models import *
from customers.models import *
import datetime
import uuid

# Create your models here.

class InMethodValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class SmsEnabledValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class E911EnabledBilledValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class Did(models.Model):
    did = models.BigIntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_dids', to_field='record_id')
    reseller = models.CharField(max_length=200, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    voice_carrier = models.ForeignKey(Voice_Carrier, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    sms_carrier = models.ForeignKey(SMS_Carrier, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    sms_type = models.ForeignKey(SMS_Type, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    term_location = models.ForeignKey(Term_Location, on_delete=models.CASCADE, null=True, blank=True, to_field='record_id')
    in_method = models.CharField(max_length=3, choices=InMethodValues.choices, null=True, blank=True)
    change_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    sms_enabled = models.CharField(max_length=3, choices=SmsEnabledValues.choices, null=True, blank=True)
    sms_campaign = models.CharField(max_length=20, null=True, blank=True)
    user_first_name = models.CharField(max_length=50, null=True, blank=True)
    user_last_name = models.CharField(max_length=50, null=True, blank=True)
    extension = models.BigIntegerField(null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    onboard_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    note = models.TextField(max_length=255, null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=3, choices=E911EnabledBilledValues.choices, null=True, blank=True)
    e911_cid = models.BigIntegerField(null=True, blank=True)
    e911_address = models.TextField(max_length=150, null=True, blank=True)
    did_uuid = models.UUIDField(max_length=50, default=uuid.uuid4(), unique=True)
    service_1 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='service_1', to_field='record_id')
    service_2 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='service_2', to_field='record_id')
    service_3 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='service_3', to_field='record_id')
    service_4 = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='service_4', to_field='record_id')
    updated_date_time = models.DateField('%m/%d/%Y %H:%M:%S', default=datetime.datetime.now, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)


class Did_Error(models.Model):
    did = models.CharField(max_length=50, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    reseller = models.CharField(max_length=200, null=True, blank=True)
    in_method = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    change_date = models.CharField(max_length=10, null=True, blank=True)
    voice_carrier = models.CharField(max_length=30, null=True, blank=True)
    sms_enabled = models.CharField(max_length=10, null=True, blank=True)
    sms_carrier = models.CharField(max_length=10, null=True, blank=True)
    sms_type = models.CharField(max_length=30, null=True, blank=True)
    sms_campaign = models.CharField(max_length=30, null=True, blank=True)
    term_location = models.CharField(max_length=30, null=True, blank=True)
    user_first_name = models.CharField(max_length=30, null=True, blank=True)
    user_last_name = models.CharField(max_length=30, null=True, blank=True)
    extension = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    onboard_date = models.CharField(max_length=30, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=10, null=True, blank=True)
    e911_cid = models.CharField(null=True, blank=True)
    e911_address = models.CharField(max_length=150, null=True, blank=True)
    did_uuid = models.CharField(max_length=50, unique=True)
    service_1 = models.CharField(max_length=100, null=True, blank=True)
    service_2 = models.CharField(max_length=100, null=True, blank=True)
    service_3 = models.CharField(max_length=100, null=True, blank=True)
    service_4 = models.CharField(max_length=100, null=True, blank=True)
    updated_date_time = models.CharField(max_length=30, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
