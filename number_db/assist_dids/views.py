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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
import requests
import os

# Create your views here.

@login_required
def did_status_service(request):
    service_size = request.GET.get('service_size', 10)
    page_number = request.GET.get('service_page')
    status = Status.objects.all().values()
    services_data = Service.objects.all().values()
    paginator = Paginator(services_data, service_size)

    services = paginator.get_page(page_number)

    return render(request, 'status_service.html', { 'status': status, 'services': services })


@login_required
def did_voice_sms_carrier_customer_type(request):
    voice_carrier = Voice_Carrier.objects.all().values()
    customer_type = Customer_Type.objects.all().values()

    return render(request, 'voice_sms_carrier_customer_type.html', {'voice_carrier': voice_carrier, 'customer_type': customer_type })


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
                name = request.POST['name']
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
        status = Status.objects.get(id=id)
    except Exception as e:
        messages.warning(request, e)

    return JsonResponse({'id':status.id, 'name': status.name})


@login_required
def did_service_status_update(request, id):
    if request.method == "POST":
        try:
            status = Status.objects.get(id=id)
            
            if not request.POST['name'] == status.name: status.is_synced = False
            
            status.name = request.POST['name']
            status.save()
            messages.success(request, 'The service status was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_service')
    

@login_required
def did_service_status_delete(request, id):
    try:
        status = Status.objects.get(id=id)
        status.is_active = False
        status.is_synced = False
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
                description = request.POST['description']
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
        try:
            service_item = Service.objects.get(id=id)
            
            if not (service_item.name == request.POST['name'] or service_item.description == request.POST['description']): service_item.is_synced = False
            
            service_item.name = request.POST['name']
            service_item.description = request.POST['description']
            service_item.save()
            messages.success(request, 'The service item was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_status_service')
    

@login_required
def did_service_item_delete(request, id):
    try:
        service_item = Service.objects.get(id=id)
        service_item.is_synced = False
        service_item.is_active = False
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
                name = request.POST['name']
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
        try:
            voice_carrier = Voice_Carrier.objects.get(id=id)
            if not voice_carrier.name == request.POST['name']: voice_carrier.is_synced = False
            voice_carrier.name = request.POST['name']
            voice_carrier.save()
            messages.success(request, 'The voice carrier was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier_customer_type')
    

@login_required
def did_voice_carrier_delete(request, id):
    try:
        voice_carrier = Voice_Carrier.objects.get(id=id)
        voice_carrier.is_synced = False
        voice_carrier.is_active = False
        voice_carrier.save()
        messages.success(request, 'The voice carrier was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_customer_type_add(request):
    if request.method == 'POST':
        try:
            customer_type = Customer_Type(
                name = request.POST['name']
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
        try:
            customer_type = Customer_Type.objects.get(id=id)
            if not customer_type.name == request.POST['name']: customer_type.is_synced = False
            customer_type.name = request.POST['name']
            customer_type.save()
            messages.success(request, 'The Customer was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_voice_sms_carrier_customer_type')
    

@login_required
def did_customer_type_delete(request, id):
    try:
        customer_type = Customer_Type.objects.get(id=id)
        customer_type.is_active = False
        customer_type.is_synced = False
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
        try:
            sms_type = SMS_Type.objects.get(id=id)
            if not sms_type.name == request.POST['name']: sms_type.is_synced = False
            sms_type.name = request.POST['name']
            sms_type.save()
            messages.success(request, 'The SMS type was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_sms_type_delete(request, id):
    try:
        sms_type = SMS_Type.objects.get(id=id)
        sms_type.is_active = False
        sms_type.is_synced = False
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
        try:
            term_location = Term_Location.objects.get(id=id)
            if term_location.name == request.POST['name']: term_location.is_synced = False
            term_location.name = request.POST['name']
            term_location.save()
            messages.success(request, 'The term location was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/assist_did/did_sms_type_term_location')
    

@login_required
def did_term_location_delete(request, id):
    try:
        term_location = Term_Location.objects.get(id=id)
        term_location.is_active = False
        term_location.is_synced = False
        term_location.save()
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
        params = {'skip': skip, 'top': top, 'select':'MITypeName,RecordID,MIIsActive', 'filter': 'MIIsActive eq true'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = Status.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['MITypeName']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = Status(
                    name = item['MITypeName'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
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
        params = {'skip': skip, 'top': top, 'select':'FullName,RecordID,SalesDesc,IsActive', 'filter': 'IsActive eq true', 'filter': 'IsActive eq true'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}Item", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = Service.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['FullName']
                        find_one.description = item['SalesDesc']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = Service(
                    name = item['FullName'],
                    description = item['SalesDesc'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
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
        params = {'skip': skip, 'top': top, 'select':'RecordID,MISMSType,MIIsActive', 'filter': 'MIIsActive eq true'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MISMSType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = SMS_Type.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['MISMSType']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = SMS_Type(
                    name = item['MISMSType'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
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

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = Term_Location.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['MITermLocation']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = Term_Location(
                    name = item['MITermLocation'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
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
        params = {'skip': skip, 'top': top, 'select':'MIVoiceCarrierName,MIIsActive,RecordID', 'filter': 'MIIsActive eq true'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = Voice_Carrier.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['MIVoiceCarrierName']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = Voice_Carrier(
                    name = item['MIVoiceCarrierName'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
                    save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100

    messages.success(request, "Voice carrier data has been synchronized with Method.")
    
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sync_customer_type_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'FullName,IsActive,RecordID', 'filter': 'IsActive eq true'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}CustomerType", headers=headers, params=params)

        if response.status_code != 200:
            messages.warning(request, f"Error {response.status_code} when getting data from API.")
            break

        response_json = response.json()

        if 'value' not in response_json:
            messages.warning(request, "Unexpected response structure from API.")
            break

        if(response_json['count'] == 0):
            break
        for item in response_json['value']:
            try:
                try:
                    find_one = Customer_Type.objects.get(record_id = item['RecordID'])
                    if find_one.is_synced == True:
                        find_one.name = item['FullName']
                        find_one.is_active = True
                    find_one.save()
                except Exception:
                    save_data = Customer_Type(
                    name = item['FullName'],
                    record_id = item['RecordID'],
                    is_synced = True,
                    )
                    save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Customer type data has been synchronized with Method.")
    
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sync_status_to_method(request):
    unsync_data = Status.objects.filter(is_synced=False)
    try:
        for item in unsync_data:
            if item.is_active == False:
                if item.record_id == None:
                    item.delete()
                else:
                    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
                    response = requests.request("DELETE", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIType/{item.record_id}", headers=headers)
                    
                    if response.status_code == 204:
                        item.delete()
                    else:
                        messages.warning(request, response.json()['title'])
            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'APIKey ' + os.getenv('METHOD_API_KEY')
                    }
                if item.record_id == None:
                    payload = '{\r\n    "MITypeName": "'+ item.name + '",\r\n    "MIIsActive": "TRUE"\r\n}'
                    response = requests.request("POST", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIType", headers = headers, data = payload)
                    
                    if response.status_code == 201:
                        item.record_id = response.json()
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

                else:
                    payload = '{ "MITypeName": "'+ item.name + '" }'
                    response = requests.request("PATCH", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIType/{item.record_id}", headers = headers, data = payload)
                    
                    if response.status_code == 204:
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

        messages.success(request, "Service Status was synced to Method")
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_status_service')


@login_required
def did_sync_sms_type_to_method(request):
    unsync_data = SMS_Type.objects.filter(is_synced=False)
    try:
        for item in unsync_data:
            if item.is_active == False:
                if item.record_id == None:
                    item.delete()
                else:
                    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
                    response = requests.request("DELETE", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MISMSType/{item.record_id}", headers=headers)
                    
                    if response.status_code == 204:
                        item.delete()
                    else:
                        messages.warning(request, response.json()['title'])
            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'APIKey ' + os.getenv('METHOD_API_KEY')
                    }
                if item.record_id == None:
                    payload = '{\r\n    "MISMSType": "'+ item.name + '",\r\n    "MIIsActive": "TRUE"\r\n}'
                    response = requests.request("POST", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MISMSType", headers = headers, data = payload)
                    
                    if response.status_code == 201:
                        item.record_id = response.json()
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

                else:
                    payload = '{ "MISMSType": "'+ item.name + '" }'
                    response = requests.request("PATCH", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MISMSType/{item.record_id}", headers = headers, data = payload)
                    
                    if response.status_code == 204:
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

        messages.success(request, "SMS type was synced to Method")
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sync_term_location_to_method(request):
    unsync_data = Term_Location.objects.filter(is_synced=False)
    try:
        for item in unsync_data:
            if item.is_active == False:
                if item.record_id == None:
                    item.delete()
                else:
                    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
                    response = requests.request("DELETE", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MITermLocation/{item.record_id}", headers=headers)
                    
                    if response.status_code == 204:
                        item.delete()
                    else:
                        messages.warning(request, response.json()['title'])
            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'APIKey ' + os.getenv('METHOD_API_KEY')
                    }
                if item.record_id == None:
                    payload = '{ "MITermLocation": "'+ item.name + '" }'
                    response = requests.request("POST", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MITermLocation", headers = headers, data = payload)
                    
                    if response.status_code == 201:
                        item.record_id = response.json()
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

                else:
                    payload = '{ "MITypeName": "'+ item.name + '" }'
                    response = requests.request("PATCH", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MITermLocation/{item.record_id}", headers = headers, data = payload)
                    
                    if response.status_code == 204:
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

        messages.success(request, "Term Location was synced to Method")
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_sms_type_term_location')


@login_required
def did_sync_voice_carrier_to_method(request):
    unsync_data = Voice_Carrier.objects.filter(is_synced=False)
    try:
        for item in unsync_data:
            if item.is_active == False:
                if item.record_id == None:
                    item.delete()
                else:
                    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
                    response = requests.request("DELETE", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier/{item.record_id}", headers=headers)
                    
                    if response.status_code == 204:
                        item.delete()
                    else:
                        messages.warning(request, response.json()['title'])
            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'APIKey ' + os.getenv('METHOD_API_KEY')
                    }
                if item.record_id == None:
                    payload = '{\r\n    "MIVoiceCarrierName": "'+ item.name + '",\r\n    "MIIsActive": "TRUE"\r\n}'
                    response = requests.request("POST", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier", headers = headers, data = payload)
                    
                    if response.status_code == 201:
                        item.record_id = response.json()
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

                else:
                    payload = '{ "MIVoiceCarrierName": "'+ item.name + '" }'
                    response = requests.request("PATCH", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MIVoiceCarrier/{item.record_id}", headers = headers, data = payload)
                    
                    if response.status_code == 204:
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

        messages.success(request, "Voice Carrier was synced to Method")
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')


@login_required
def did_sync_customer_type_to_method(request):
    unsync_data = Customer_Type.objects.filter(is_synced=False)
    try:
        for item in unsync_data:
            if item.is_active == False:
                if item.record_id == None:
                    item.delete()
                else:
                    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
                    response = requests.request("DELETE", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}CustomerType/{item.record_id}", headers=headers)
                    
                    if response.status_code == 204:
                        item.delete()
                    else:
                        messages.warning(request, response.json()['title'])
            else:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'APIKey ' + os.getenv('METHOD_API_KEY')
                    }
                if item.record_id == None:
                    payload = '{\r\n    "FullName": "'+ item.name + '",\r\n    "IsActive": "TRUE"\r\n}'
                    response = requests.request("POST", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}CustomerType", headers = headers, data = payload)
                    
                    if response.status_code == 201:
                        item.record_id = response.json()
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

                else:
                    payload = '{ "FullName": "'+ item.name + '" }'
                    response = requests.request("PATCH", f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}CustomerType/{item.record_id}", headers = headers, data = payload)
                    
                    if response.status_code == 204:
                        item.is_synced = True
                        item.save()
                    else:
                        messages.warning(request, response.json()['title'])

        messages.success(request, "Customer Type was synced to Method")
    except Exception as e:
        messages.warning(request, e)
    return redirect('/assist_did/did_voice_sms_carrier_customer_type')
