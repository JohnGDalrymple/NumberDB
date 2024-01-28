from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ServiceTypeValues(models.TextChoices):
    FUSION = 'F', _('Fusion')
    TEAMS = 'T', _('Teams')
    HOSTED_SMS = 'HS', _('Hosted SMS')
    PARKED = 'PK', _('Parked')
    INVENTORY = 'IV', _('Inventory')
    EFAX = 'EF', _('Efax')
    ORPHANED = 'OP', _('Orphaned')
    COMELIT = 'CL', _('Comelit')


class VoiceCarrierValues(models.TextChoices):
    INTQ_WHOLESALE = 'IW', _('INTQ - Wholesale')
    INTQ_OC = 'IO', _('INTQ - OC')
    TWILIO = 'TWI', _('Twilio')


class SmsCarrierValues(models.TextChoices):
    INTQ = 'INTQ', _('INTQ')
    TWILIO = 'TWL', _('Twilio')


class StatusValues(models.TextChoices):
    ACTIVE = 'A', _('Active')
    DISCO = 'D', _('Disco')


class InMethodValues(models.TextChoices):
    YES = 'Y', _('Yes')
    NO = 'N', _('No')


class SmsEnabledValues(models.TextChoices):
    YES = 'Y', _('Yes')
    NO = 'N', _('No')


class E911EnabledBilledValues(models.TextChoices):
    YES = 'Y', _('Yes')
    NO = 'N', _('No')


class SmsTypeValues(models.TextChoices):
    YAK_PERSONAL = 'YP', _('Yak Personal')
    YAK_SHARED = 'YS', _('Yak Shared')
    YAK_BOTH = 'YB', _('Yak Personal and Shared')
    INTQ_API = 'IA', _('INTQ API')
    CLERK = 'CL', _('Clerk')
    SIPS = 'SI', _('SIP/Simple')


class TermLocationValues(models.TextChoices):
    SBC_EAST = 'SE', _('SBC - East')
    SBC_WEST = 'SW', _('SBC - West')
    HOSTED_EAST = 'HE', _('Hosted - East')
    HOSTED_WEST = 'HW', _('Hosted - West')
    OC_OPERATOR_CONNECT = 'OC', _('OP - Operator Connect')


class Did(models.Model):
    did = models.BigIntegerField()
    customer = models.CharField(max_length=30, null=True, blank=True)
    reseller = models.CharField(max_length=30, null=True, blank=True)
    in_method = models.CharField(max_length=2, choices=InMethodValues.choices, null=True, blank=True)
    status = models.CharField(max_length=2, choices=StatusValues.choices, null=True, blank=True)
    change_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    voice_carrier = models.CharField(max_length=3, choices=VoiceCarrierValues.choices, null=True, blank=True)
    type = models.CharField(max_length=2, choices=ServiceTypeValues.choices, null=True, blank=True)
    sms_enabled = models.CharField(max_length=2, choices=SmsEnabledValues.choices, null=True, blank=True)
    sms_carrier = models.CharField(max_length=4, choices=SmsCarrierValues.choices, null=True, blank=True)
    sms_type = models.CharField(max_length=2, choices=SmsTypeValues.choices, null=True, blank=True)
    sms_campaign = models.CharField(max_length=20, null=True, blank=True)
    term_location = models.CharField(max_length=2, choices=TermLocationValues.choices, null=True, blank=True)
    user_first_name = models.CharField(max_length=30, null=True, blank=True)
    user_last_name = models.CharField(max_length=30, null=True, blank=True)
    extension = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    onboard_date = models.DateField('%m/%d/%Y', null=True, blank=True)
    note = models.TextField(max_length=255, null=True, blank=True)
    e911_enabled_billed = models.CharField(max_length=2, choices=E911EnabledBilledValues.choices, null=True, blank=True)
    e911_cid = models.BigIntegerField(null=True, blank=True)
    e911_address = models.TextField(max_length=150, null=True, blank=True)
    did_uuid = models.TextField(max_length=50, unique=True)
    service_1 = models.TextField(max_length=100, null=True, blank=True)
    service_2 = models.TextField(max_length=100, null=True, blank=True)
    service_3 = models.TextField(max_length=100, null=True, blank=True)
    service_4 = models.TextField(max_length=100, null=True, blank=True)
    updated_date_time = models.DateField('%m/%d/%Y %H:%M:%S', null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
