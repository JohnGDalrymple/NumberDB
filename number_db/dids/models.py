from django.db import models
from django.utils.translation import gettext_lazy as _
from assist_dids.models import *
from customers.models import *
from django.db.models import Q
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
    did = models.BigIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_dids')
    reseller = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='reseller_dids')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey(Service_Type, on_delete=models.CASCADE, null=True, blank=True)
    voice_carrier = models.ForeignKey(Voice_Carrier, on_delete=models.CASCADE, null=True, blank=True)
    sms_carrier = models.ForeignKey(SMS_Carrier, on_delete=models.CASCADE, null=True, blank=True)
    sms_type = models.ForeignKey(SMS_Type, on_delete=models.CASCADE, null=True, blank=True)
    term_location = models.ForeignKey(Term_Location, on_delete=models.CASCADE, null=True, blank=True)
    in_method = models.CharField(max_length=3, choices=InMethodValues.choices, null=True, blank=True)
    change_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    sms_enabled = models.CharField(max_length=3, choices=SmsEnabledValues.choices, null=True, blank=True)
    sms_campaign = models.CharField(max_length=20, null=True, blank=True)
    user_first_name = models.CharField(max_length=30, null=True, blank=True)
    user_last_name = models.CharField(max_length=30, null=True, blank=True)
    extension = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    onboard_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    note = models.TextField(max_length=255, null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=3, choices=E911EnabledBilledValues.choices, null=True, blank=True)
    e911_cid = models.BigIntegerField(null=True, blank=True)
    e911_address = models.TextField(max_length=150, null=True, blank=True)
    did_uuid = models.UUIDField(max_length=50, default=uuid.uuid4(), unique=True)
    service_1 = models.TextField(max_length=100, null=True, blank=True)
    service_2 = models.TextField(max_length=100, null=True, blank=True)
    service_3 = models.TextField(max_length=100, null=True, blank=True)
    service_4 = models.TextField(max_length=100, null=True, blank=True)
    updated_date_time = models.DateField('%m/%d/%Y %H:%M:%S', default=datetime.datetime.now, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)

    def search(self, query):
        qs = self.objects.filter(
            Q(did__icontains=query)|
            Q(customer__full_name__icontains=query)|
            Q(reseller__full_name__icontains=query)|
            Q(in_method__iexact=query)|
            Q(status__name__icontains=query)|
            Q(service_type__name__icontains=query)|
            Q(voice_carrier__name__icontains=query)|
            Q(sms_carrier__name__icontains=query)|
            Q(sms_type__name__icontains=query)|
            Q(sms_campaign__icontains=query)|
            Q(term_location__name__icontains=query)|
            Q(user_first_name__icontains=query)|
            Q(user_last_name__icontains=query)|
            Q(extension__icontains=query)|
            Q(email__icontains=query)|
            Q(note__icontains=query)
        )
        return qs


class Did_Error(models.Model):
    did = models.CharField(max_length=50, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    reseller = models.CharField(max_length=200, null=True, blank=True)
    in_method = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    change_date = models.CharField(max_length=10, null=True, blank=True)
    voice_carrier = models.CharField(max_length=30, null=True, blank=True)
    type = models.CharField(max_length=30, null=True, blank=True)
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
