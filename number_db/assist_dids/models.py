from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class Voice_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class SMS_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class Customer_Type(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class SMS_Type(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class Term_Location(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)

class Service(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    record_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_synced = models.BooleanField(default=False)