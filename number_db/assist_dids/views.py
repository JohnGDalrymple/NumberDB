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
import requests
import os

# Create your views here.

@login_required
def did_status_service(request):
    status = Status.objects.all().values()
    services = Service.objects.all().values()

    return render(request, 'status_service.html', { 'status': status, 'services': services })


@login_required
def did_voice_sms_carrier_customer_type(request):
    sms_carrier = SMS_Carrier.objects.all().values()
    voice_carrier = Voice_Carrier.objects.all().values()
    customer_type = Customer_Type.objects.all().values()

    return render(request, 'voice_sms_carrier_customer_type.html', { 'sms_carrier': sms_carrier, 'voice_carrier': voice_carrier, 'customer_type': customer_type })


@login_required
def did_sms_type_term_location(request):
    sms_type = SMS_Type.objects.all().values()
    term_location = Term_Location.objects.all().values()

    return render(request, 'sms_type_term_location.html', { 'sms_type': sms_type, 'term_location': term_location })


@login_required
def did_service_status_add(request):
    if request.method == 'POST':
        try:
            service_status = Status(
                name = request.POST['name'],
                is_active = True
            )
            service_status.full_clean()
            service_status.save()
            messages.success(request, 'Service status was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_status_service')


@login_required
def did_service_status_read(request, id):
    try:
        status = Status.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':status.id, 'name': status.name})


@login_required
def did_service_status_update(request, id):
    if request.method == "POST":
        status = Status.objects.get(id=id)
        status.name = request.POST['name']
        try:
            status.save()
            messages.success(request, 'The service status was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_service')
    

@login_required
def did_service_status_delete(request, id):
    status = Status.objects.get(id=id)
    status.name = status.name + " (deleted)"
    status.is_active = False
    try:
        status.save()
        messages.success(request, 'The service status was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_status_service')


@login_required
def did_service_item_add(request):
    if request.method == 'POST':
        try:
            service_item = Service(
                name = request.POST['name'],
                description = request.POST['description'],
                is_active = True
            )
            service_item.full_clean()
            service_item.save()
            messages.success(request, 'Service item was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_status_service')


@login_required
def did_service_item_read(request, id):
    try:
        service_item = Service.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':service_item.id, 'name': service_item.name, 'description': service_item.description})


@login_required
def did_service_item_update(request, id):
    if request.method == "POST":
        service_item = Service.objects.get(id=id)
        service_item.name = request.POST['name']
        service_item.description = request.POST['description']
        try:
            service_item.save()
            messages.success(request, 'The service item was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_service')
    

@login_required
def did_service_item_delete(request, id):
    service_item = Service.objects.get(id=id)
    service_item.name = service_item.name + " (deleted)"
    service_item.is_active = False
    try:
        service_item.save()
        messages.success(request, 'The service item was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_status_service')


@login_required
def did_voice_carrier_add(request):
    if request.method == 'POST':
        try:
            voice_carrier = Voice_Carrier(
                name = request.POST['name'],
                is_active = True
            )
            voice_carrier.full_clean()
            voice_carrier.save()
            messages.success(request, 'Voice carrier was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_voice_carrier_read(request, id):
    try:
        voice_carrier = Voice_Carrier.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':voice_carrier.id, 'name': voice_carrier.name})


@login_required
def did_voice_carrier_update(request, id):
    if request.method == "POST":
        voice_carrier = Voice_Carrier.objects.get(id=id)
        voice_carrier.name = request.POST['name']
        try:
            voice_carrier.save()
            messages.success(request, 'The voice carrier was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier_customer_type')
    

@login_required
def did_voice_carrier_delete(request, id):
    voice_carrier = Voice_Carrier.objects.get(id=id)
    voice_carrier.name = voice_carrier.name + " (deleted)"
    voice_carrier.is_active = False
    try:
        voice_carrier.save()
        messages.success(request, 'The voice carrier was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sms_carrier_add(request):
    if request.method == 'POST':
        try:
            sms_carrier = SMS_Carrier(
                name = request.POST['name'],
                is_active = True
            )
            sms_carrier.full_clean()
            sms_carrier.save()
            messages.success(request, 'SMS carrier was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sms_carrier_read(request, id):
    try:
        sms_carrier = SMS_Carrier.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':sms_carrier.id, 'name': sms_carrier.name})


@login_required
def did_sms_carrier_update(request, id):
    if request.method == "POST":
        sms_carrier = SMS_Carrier.objects.get(id=id)
        sms_carrier.name = request.POST['name']
        try:
            sms_carrier.save()
            messages.success(request, 'The SMS carrier was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier_customer_type')
    

@login_required
def did_sms_carrier_delete(request, id):
    sms_carrier = SMS_Carrier.objects.get(id=id)
    sms_carrier.name = sms_carrier.name + " (deleted)"
    sms_carrier.is_active = False
    try:
        sms_carrier.save()
        messages.success(request, 'The SMS carrier was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_customer_type_add(request):
    if request.method == 'POST':
        try:
            customer_type = Customer_Type(
                name = request.POST['name'],
                is_active = True
            )
            customer_type.full_clean()
            customer_type.save()
            messages.success(request, 'Customer type was created successfully!')
        except Exception as e:
            messages.warning(request, e)

        return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_customer_type_read(request, id):
    try:
        customer_type = Customer_Type.objects.get(id = id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':customer_type.id, 'name': customer_type.name})


@login_required
def did_customer_type_update(request, id):
    if request.method == "POST":
        customer_type = Customer_Type.objects.get(id=id)
        customer_type.name = request.POST['name']
        try:
            customer_type.save()
            messages.success(request, 'The Customer was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier_customer_type')
    

@login_required
def did_customer_type_delete(request, id):
    customer_type = Customer_Type.objects.get(id=id)
    customer_type.name = customer_type.name + " (deleted)"
    customer_type.is_active = False
    try:
        customer_type.save()
        messages.success(request, 'The Customer type was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sms_type_add(request):
    if request.method == 'POST':
        try:
            sms_type = SMS_Type(
                name = request.POST['name'],
                is_active = True
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

    return JsonResponse({'id':sms_type.id, 'name': sms_type.name})


@login_required
def did_sms_type_update(request, id):
    if request.method == "POST":
        sms_type = SMS_Type.objects.get(id=id)
        sms_type.name = request.POST['name']
        try:
            sms_type.save()
            messages.success(request, 'The SMS type was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_sms_type_delete(request, id):
    sms_type = SMS_Type.objects.get(id=id)
    sms_type.name = sms_type.name + " (deleted)"
    sms_type.is_active = False
    try:
        sms_type.save()
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

    return JsonResponse({'id':term_location.id, 'name': term_location.name})


@login_required
def did_term_location_update(request, id):
    if request.method == "POST":
        term_location = Term_Location.objects.get(id=id)
        term_location.name = request.POST['name']
        try:
            term_location.save()
            messages.success(request, 'The term location was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_term_location_delete(request, id):
    term_location = Term_Location.objects.get(id=id)
    try:
        term_location.delete()
        messages.success(request, 'The term location was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sync_status_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'MITypeName,RecordID,MIIsActive'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = Status(
            name = item['MITypeName'],
            record_id = item['RecordID'],
            is_active = item['MIIsActive'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Service Status has been synchronized with Method.")
        
    return redirect('/assist_did/did_status_service')


@login_required
def did_sync_service_item_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'FullName,RecordID,SalesDesc,IsActive'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}Item", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = Service(
            name = item['FullName'],
            description = item['SalesDesc'],
            record_id = item['RecordID'],
            is_active = item['IsActive'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Service Item data has been synchronized with Method.")
        
    return redirect('/assist_did/did_status_service')


@login_required
def did_sync_sms_type_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'RecordID,MISMSType,MIIsActive'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MISMSType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = SMS_Type(
            name = item['MISMSType'],
            record_id = item['RecordID'],
            is_active = item['MIIsActive'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100

    messages.success(request, "SMS Type data has been synchronized with Method.")
    
    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sync_term_location_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'RecordID,MITermLocation'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MITermLocation", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = Term_Location(
            name = item['MITermLocation'],
            record_id = item['RecordID'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Term location data has been synchronized with Method.")

    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sync_voice_carrier_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'MIVoiceCarrierName,MIIsActive,RecordID'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = Voice_Carrier(
            name = item['MIVoiceCarrierName'],
            is_active = item['MIIsActive'],
            record_id = item['RecordID'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100

    messages.success(request, "Voice carrier data has been synchronized with Method.")
    
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sync_sms_carrier_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'MIVoiceCarrierName,MIIsActive,RecordID'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = SMS_Carrier(
            name = item['MIVoiceCarrierName'],
            is_active = item['MIIsActive'],
            record_id = item['RecordID'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "SMS carrier data has been synchronized with Method.")
    
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sync_customer_type_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'FullName,IsActive,RecordID'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}CustomerType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(len(response_json['value']) == 0):
            break
        for item in response_json['value']:
            save_data = Customer_Type(
            name = item['FullName'],
            is_active = item['IsActive'],
            record_id = item['RecordID'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Customer type data has been synchronized with Method.")
    
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')