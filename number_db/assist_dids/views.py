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
def did_status(request):
    status = Status.objects.all().values()
    return render(request, 'status.html', { 'status': status })


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
def did_service_type_read(request, id):
    try:
        service_type = Service_Type.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':service_type.id, 'name': service_type.name, 'description': service_type.description})


@login_required
def did_service_type_update(request, id):
    if request.method == "POST":
        service_type = Service_Type.objects.get(id=id)
        service_type.name = request.POST['name']
        service_type.description = request.POST['description']
        try:
            service_type.save()
            messages.success(request, 'The service type was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_type')
    

@login_required
def did_service_type_delete(request, id):
    service_type = Service_Type.objects.get(id=id)
    service_type.delete()
    try:
        messages.success(request, 'The service type was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_status_type')
    

@login_required
def did_service_status_add(request):
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


@login_required
def did_voice_carrier_add(request):
    if request.method == 'POST':
        try:
            voice_carrier = Voice_Carrier(
                name = request.POST['name'],
                description = request.POST['description'],
            )
            voice_carrier.full_clean()
            voice_carrier.save()
            messages.success(request, 'Voice carrier was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_voice_sms_carrier')


@login_required
def did_voice_carrier_read(request, id):
    try:
        voice_carrier = Voice_Carrier.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':voice_carrier.id, 'name': voice_carrier.name, 'description': voice_carrier.description})


@login_required
def did_voice_carrier_update(request, id):
    if request.method == "POST":
        voice_carrier = Voice_Carrier.objects.get(id=id)
        voice_carrier.name = request.POST['name']
        voice_carrier.description = request.POST['description']
        try:
            voice_carrier.save()
            messages.success(request, 'The voice carrier was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier')
    

@login_required
def did_voice_carrier_delete(request, id):
    voice_carrier = Voice_Carrier.objects.get(id=id)
    voice_carrier.delete()
    try:
        messages.success(request, 'The voice carrier was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier')


@login_required
def did_sms_carrier_add(request):
    if request.method == 'POST':
        try:
            sms_carrier = SMS_Carrier(
                name = request.POST['name'],
                description = request.POST['description'],
            )
            sms_carrier.full_clean()
            sms_carrier.save()
            messages.success(request, 'SMS carrier was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_voice_sms_carrier')


@login_required
def did_sms_carrier_read(request, id):
    try:
        sms_carrier = SMS_Carrier.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':sms_carrier.id, 'name': sms_carrier.name, 'description': sms_carrier.description})


@login_required
def did_sms_carrier_update(request, id):
    if request.method == "POST":
        sms_carrier = SMS_Carrier.objects.get(id=id)
        sms_carrier.name = request.POST['name']
        sms_carrier.description = request.POST['description']
        try:
            sms_carrier.save()
            messages.success(request, 'The SMS carrier was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier')
    

@login_required
def did_sms_carrier_delete(request, id):
    sms_carrier = SMS_Carrier.objects.get(id=id)
    sms_carrier.delete()
    try:
        messages.success(request, 'The SMS carrier was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier')


@login_required
def did_sms_type_add(request):
    if request.method == 'POST':
        try:
            sms_type = SMS_Type(
                name = request.POST['name'],
                description = request.POST['description'],
            )
            sms_type.full_clean()
            sms_type.save()
            messages.success(request, 'SMS type was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sms_type_read(request, id):
    try:
        sms_type = SMS_Type.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':sms_type.id, 'name': sms_type.name, 'description': sms_type.description})


@login_required
def did_sms_type_update(request, id):
    if request.method == "POST":
        sms_type = SMS_Type.objects.get(id=id)
        sms_type.name = request.POST['name']
        sms_type.description = request.POST['description']
        try:
            sms_type.save()
            messages.success(request, 'The SMS type was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_sms_type_delete(request, id):
    sms_type = SMS_Type.objects.get(id=id)
    sms_type.delete()
    try:
        messages.success(request, 'The SMS type was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_term_location_add(request):
    if request.method == 'POST':
        try:
            term_location = Term_Location(
                name = request.POST['name'],
                description = request.POST['description'],
            )
            term_location.full_clean()
            term_location.save()
            messages.success(request, 'Term location was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_term_location_read(request, id):
    try:
        term_location = Term_Location.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':term_location.id, 'name': term_location.name, 'description': term_location.description})


@login_required
def did_term_location_update(request, id):
    if request.method == "POST":
        term_location = Term_Location.objects.get(id=id)
        term_location.name = request.POST['name']
        term_location.description = request.POST['description']
        try:
            term_location.save()
            messages.success(request, 'The term location was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_term_location_delete(request, id):
    term_location = Term_Location.objects.get(id=id)
    term_location.delete()
    try:
        messages.success(request, 'The term location was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_sms_type_term_location')