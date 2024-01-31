from django.db import models

# Create your models here.

class Customer(models.Model):
    full_name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    billing_address = models.CharField(max_length=150, null=True, blank=True)
    billing_city = models.CharField(max_length=50, null=True, blank=True)
    billing_state = models.CharField(max_length=10, null=True, blank=True)
    billing_zipcode = models.CharField(max_length=20, null=True, blank=True)
    billing_country = models.CharField(max_length=20, null=True, blank=True)
    e911_address = models.CharField(max_length=150, null=True, blank=True)
    e911_city = models.CharField(max_length=50, null=True, blank=True)
    e911_state = models.CharField(max_length=10, null=True, blank=True)
    e911_zipcode = models.CharField(max_length=20, null=True, blank=True)
    e911_country = models.CharField(max_length=20, null=True, blank=True)