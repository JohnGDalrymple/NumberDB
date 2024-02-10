from django.shortcuts import render, redirect
import csv
from .models import *
from django.db.models import Q
from customers.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.http import JsonResponse
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

    return render(request, 'status_type.html', { 'status': status, 'types': types })


@login_required
def did_voice_sms_carrier(request):
    sms_carrier = SMS_Carrier.objects.all().values()
    voice_carrier = Voice_Carrier.objects.all().values()

    return render(request, 'voice_sms_carrier.html', { 'sms_carrier': sms_carrier, 'voice_carrier': voice_carrier })


@login_required
def did_sms_type_term_location(request):
    sms_type = SMS_Type.objects.all().values()
    term_location = Term_Location.objects.all().values()

    return render(request, 'sms_type_term_location.html', { 'sms_type': sms_type, 'term_location': term_location })


@login_required
def did_serivce_type_add(request):
    if request.method == 'POST':
        try:
            service_type = Service_Type(
                name = request.POST['name'],
                description = request.POST['description'],
                )
            service_type.full_clean()
        except Exception as e:
            messages.warning(request, e)

        service_type.save()
        messages.success(request, 'Service type was created successfully!')
        return redirect('/assist_did/did_status_type')
    

@login_required
def did_serivce_status_add(request):
    if request.method == 'POST':
        try:
            service_status = Status(
                name = request.POST['name'],
                description = request.POST['description'],
            )
            service_status.full_clean()
            service_status.save()
            messages.success(request, 'Service status was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_status_type')


@login_required
def did_service_status_read(request, id):
    try:
        status = Status.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':status.id, 'name': status.name, 'description': status.description})


@login_required
def did_service_status_update(request, id):
    if request.method == "POST":
        status = Status.objects.get(id=id)
        status.name = request.POST['name']
        status.description = request.POST['description']
        try:
            status.save()
            messages.success(request, 'The service status was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_type')
    

@login_required
def did_service_status_delete(request, id):
    status = Status.objects.get(id=id)
    status.delete()
    try:
        messages.success(request, 'The service status was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_status_type')