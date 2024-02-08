from django.shortcuts import render, redirect
import csv
from .models import *
from django.db.models import Q
from customers.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
import unicodedata
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
import uuid

# Create your views here.

@login_required
def did_status_type(request):
    status = Status.objects.all().values()
    types = Service_Type.objects.all().values()

    convert_status = []
    convert_types = []

    for item in status:
        convert_status.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })
    
    for item in types:
        convert_types.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })

    return render(request, 'status_type.html', { 'status': convert_status, 'types': convert_types })


@login_required
def did_voice_sms_carrier(request):
    sms_carrier = SMS_Carrier.objects.all().values()
    voice_carrier = Voice_Carrier.objects.all().values()

    convert_sms_carrier = []
    convert_voice_carrier = []

    for item in sms_carrier:
        convert_sms_carrier.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })
    
    for item in voice_carrier:
        convert_voice_carrier.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })

    return render(request, 'voice_sms_carrier.html', { 'sms_carrier': convert_sms_carrier, 'voice_carrier': convert_voice_carrier })


@login_required
def did_sms_type_term_location(request):
    sms_type = SMS_Type.objects.all().values()
    term_location = Term_Location.objects.all().values()

    convert_sms_type = []
    convert_term_location = []

    for item in sms_type:
        convert_sms_type.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })
    
    for item in term_location:
        convert_term_location.append({
            'name': item['name'],
            'description': item['description'] if item['description'] else '',
        })

    return render(request, 'sms_type_term_location.html', { 'sms_type': convert_sms_type, 'term_location': convert_term_location })
