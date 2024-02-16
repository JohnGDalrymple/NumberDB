from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Voice_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class SMS_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class SMS_Type(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Term_Location(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)