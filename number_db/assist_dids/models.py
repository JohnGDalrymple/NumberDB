from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

class Service_Type(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

class Voice_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

class SMS_Carrier(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

class SMS_Type(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

class Term_Location(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)