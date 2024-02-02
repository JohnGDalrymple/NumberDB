from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
import uuid

# Create your models here.

class ServiceTypeValues(models.TextChoices):
    FUSION = 'Fusion', _('Fusion')
    TEAMS = 'Teams', _('Teams')
    HOSTED_SMS = 'Hosted SMS', _('Hosted SMS')
    PARKED = 'Parked', _('Parked')
    INVENTORY = 'Inventory', _('Inventory')
    EFAX = 'Efax', _('Efax')
    ORPHANED = 'Orphaned', _('Orphaned')
    COMELIT = 'Comelit', _('Comelit')


class VoiceCarrierValues(models.TextChoices):
    INTQ_WHOLESALE = 'INTQ - Wholesale', _('INTQ - Wholesale')
    INTQ_OC = 'INTQ - OC', _('INTQ - OC')
    TWILIO = 'Twilio', _('Twilio')


class SmsCarrierValues(models.TextChoices):
    INTQ = 'INTQ', _('INTQ')
    TWILIO = 'Twilio', _('Twilio')


class StatusValues(models.TextChoices):
    ACTIVE = 'Active', _('Active')
    DISCO = 'Disco', _('Disco')


class InMethodValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class SmsEnabledValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class E911EnabledBilledValues(models.TextChoices):
    YES = 'Yes', _('Yes')
    NO = 'No', _('No')


class SmsTypeValues(models.TextChoices):
    YAK_PERSONAL = 'Yak Personal', _('Yak Personal')
    YAK_SHARED = 'Yak Shared', _('Yak Shared')
    YAK_BOTH = 'Yak Personal and Shared', _('Yak Personal and Shared')
    INTQ_API = 'INTQ API', _('INTQ API')
    CLERK = 'Clerk', _('Clerk')
    SIPS = 'SIP/Simple', _('SIP/Simple')


class TermLocationValues(models.TextChoices):
    SBC_EAST = 'SBC - East', _('SBC - East')
    SBC_WEST = 'SW', _('SBC - West')
    HOSTED_EAST = 'Hosted - East', _('Hosted - East')
    HOSTED_WEST = 'Hosted - West', _('Hosted - West')
    OC_OPERATOR_CONNECT = 'OP - Operator Connect', _('OP - Operator Connect')


class Did(models.Model):
    did = models.BigIntegerField()
    customer = models.CharField(max_length=30, null=True, blank=True)
    reseller = models.CharField(max_length=30, null=True, blank=True)
    in_method = models.CharField(max_length=3, choices=InMethodValues.choices, null=True, blank=True)
    status = models.CharField(max_length=6, choices=StatusValues.choices, null=True, blank=True)
    change_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    voice_carrier = models.CharField(max_length=16, choices=VoiceCarrierValues.choices, null=True, blank=True)
    type = models.CharField(max_length=10, choices=ServiceTypeValues.choices, null=True, blank=True)
    sms_enabled = models.CharField(max_length=3, choices=SmsEnabledValues.choices, null=True, blank=True)
    sms_carrier = models.CharField(max_length=6, choices=SmsCarrierValues.choices, null=True, blank=True)
    sms_type = models.CharField(max_length=23, choices=SmsTypeValues.choices, null=True, blank=True)
    sms_campaign = models.CharField(max_length=20, null=True, blank=True)
    term_location = models.CharField(max_length=21, choices=TermLocationValues.choices, null=True, blank=True)
    user_first_name = models.CharField(max_length=30, null=True, blank=True)
    user_last_name = models.CharField(max_length=30, null=True, blank=True)
    extension = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    onboard_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    note = models.TextField(max_length=255, null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=3, choices=E911EnabledBilledValues.choices, null=True, blank=True)
    e911_cid = models.BigIntegerField(null=True, blank=True)
    e911_address = models.TextField(max_length=150, null=True, blank=True)
    did_uuid = models.UUIDField(max_length=50,default=uuid.uuid4(), unique=True)
    service_1 = models.TextField(max_length=100, null=True, blank=True)
    service_2 = models.TextField(max_length=100, null=True, blank=True)
    service_3 = models.TextField(max_length=100, null=True, blank=True)
    service_4 = models.TextField(max_length=100, null=True, blank=True)
    updated_date_time = models.DateField('%m/%d/%Y %H:%M:%S', default=datetime.datetime.now, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
