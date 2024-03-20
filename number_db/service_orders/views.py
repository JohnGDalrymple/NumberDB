from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
import datetime
from functools import reduce
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
from operator import or_
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymsteams
import os
from django.db import transaction
import json

# Create your views here.

def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y').date() if date_string else None

default_data_header = ['username', 'email', 'number', 'texting', 'e911_number', 'e911_address', 'updated_by']

def switchStatus(value):
    if value == 0:
        return 'Created'
    elif value == 1:
        return 'Updated'
    elif value == 2:
        return 'Submitted'
    elif value == 3:
        return 'Deleted'
    elif value.lower() == 'created':
        return 0
    elif value.lower() == 'updated':
        return 1
    elif value.lower() == 'submitted':
        return 2
    elif value.lower() == 'deleted':
        return 3
    else:
        return None


@login_required
def service_order_list(request):
    if request.GET.get('search'):
        service_orders = []
        query = request.GET['search']

        q_objects = []
        q_objects.append((Q(username__icontains = query)))
        q_objects.append((Q(customer__full_name__icontains = query)))
        q_objects.append((Q(texting__icontains = query)))
        q_objects.append((Q(updated_by__icontains = query)))
        q_objects.append((Q(term_location__name__icontains = query)))
        q_objects.append((Q(number_email_dates__number__icontains = query)))
        q_objects.append((Q(number_email_dates__email__icontains = query)))
        q_objects.append((Q(number_email_dates__e911_number__icontains = query)))
        q_objects.append((Q(number_email_dates__e911_address__icontains = query)))
        q_objects.append((Q(number_email_dates__reseller__icontains = query)))
        q_objects.append((Q(number_email_dates__service_status__name__icontains = query)))
        q_objects.append((Q(number_email_dates__voice_carrier__name__icontains = query)))
        q_objects.append((Q(number_email_dates__sms_carrier__name__icontains = query)))
        q_objects.append((Q(number_email_dates__sms_type__name__icontains = query)))
        q_objects.append((Q(number_email_dates__sms_enabled__icontains = query)))
        q_objects.append((Q(number_email_dates__sms_campaign__icontains = query)))
        q_objects.append((Q(number_email_dates__user_first_name__icontains = query)))
        q_objects.append((Q(number_email_dates__user_last_name__icontains = query)))
        q_objects.append((Q(number_email_dates__extension__icontains = query)))
        q_objects.append((Q(number_email_dates__e911_enabled_billed__icontains = query)))
        q_objects.append((Q(number_email_dates__service_1__name__icontains = query)))
        q_objects.append((Q(number_email_dates__service_2__name__icontains = query)))
        q_objects.append((Q(number_email_dates__service_3__name__icontains = query)))
        q_objects.append((Q(number_email_dates__service_4__name__icontains = query)))

        service_orders = Service_Order.objects.filter(reduce(or_, q_objects)).distinct()

        for item in service_orders:
            item.texting = "" if item.texting is None else item.texting
            item.status = switchStatus(item.status)
            item.updated_by = "" if item.updated_by is None else item.updated_by
            item.number = item.number_email_dates.all().order_by('id')[0].number if item.number_email_dates.all().order_by('id')[0].number else ""
            item.email = item.number_email_dates.all().order_by('id')[0].email if item.number_email_dates.all().order_by('id')[0].email else ""
            item.requested_port_date = item.number_email_dates.all().order_by('id')[0].requested_port_date if item.number_email_dates.all().order_by('id')[0].requested_port_date else ""
        
        size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(service_orders, size)
        service_list = paginator.get_page(page_number)

        return render(request, 'service_orders.html', {'service_orders': service_list, 'search': query})
    else:
        service_orders = Service_Order.objects.all()
    
        for item in service_orders:
            item.texting = "" if item.texting is None else item.texting
            item.status = switchStatus(item.status)
            item.updated_by = "" if item.updated_by is None else item.updated_by
            item.number = item.number_email_dates.all().order_by('id')[0].number if item.number_email_dates.all().order_by('id')[0].number else ""
            item.email = item.number_email_dates.all().order_by('id')[0].email if item.number_email_dates.all().order_by('id')[0].email else ""
            item.requested_port_date = item.number_email_dates.all().order_by('id')[0].requested_port_date if item.number_email_dates.all().order_by('id')[0].requested_port_date else ""

        size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(service_orders, size)
        service_list = paginator.get_page(page_number)
        
        return render(request, 'service_orders.html', {'service_orders': service_list})


@login_required
def service_order_delete(request, id):
    try:
        service_order = Service_Order.objects.get(id=int(id))
        service_order.status = 3
        service_order.save()
        messages.warning(request, 'The service order was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/service_order')


@login_required
def service_order_create(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            service_order = Service_Order(
                username=request_data['username'],
                customer=Customer.objects.get(record_id=int(request_data['customer'])) if request_data['customer'] else None,
                texting=request_data['texting'],
                term_location=Term_Location.objects.get(record_id=int(request_data['term_location'])) if request_data['term_location'] else None,
                updated_by=str(request.user),
            )

            service_order.full_clean()
            service_order.save()

            for item in request_data['number_email_date']:
                number_email_date_dict = {
                    'number' : int(item['number']),
                    'email' : item['email'],
                    'reseller' : item['reseller'],
                    'requested_port_date' : parse_date(item['requested_port_date']),
                    'e911_number' : int(item['e911_number']) if item['e911_number'] else None,
                    'e911_address' : item['e911_address'],
                    'service_status' : Status.objects.get(record_id=int(item['service_status'])) if item['service_status'] else None,
                    'voice_carrier' : Voice_Carrier.objects.get(record_id=int(item['voice_carrier'])) if item['voice_carrier'] else None,
                    'sms_carrier' : Voice_Carrier.objects.get(record_id=int(item['sms_carrier'])) if item['sms_carrier'] else None,
                    'sms_type' : SMS_Type.objects.get(record_id=int(item['sms_type'])) if item['sms_type'] else None,
                    'sms_enabled' : item['sms_enabled'],
                    'sms_campaign' : item['sms_campaign'],
                    'user_first_name' : item['user_first_name'],
                    'user_last_name' : item['user_last_name'],
                    'extension' : int(item['extension']) if item['extension'] else None,
                    'onboard_date' : parse_date(item['onboard_date']),
                    'e911_enabled_billed' : item['e911_enabled_billed'],
                    'service_1' : Service.objects.get(record_id=int(item['service_1'])) if item['service_1'] else None,
                    'service_2' : Service.objects.get(record_id=int(item['service_2'])) if item['service_2'] else None,
                    'service_3' : Service.objects.get(record_id=int(item['service_3'])) if item['service_3'] else None,
                    'service_4' : Service.objects.get(record_id=int(item['service_4'])) if item['service_4'] else None,
                }
                number_email_date = Number_Email_Date.objects.create(**number_email_date_dict)
                service_order.number_email_dates.add(number_email_date)

            messages.success(request, 'The service order was created successfully!')
        except Exception as e:
            messages.warning(request, f"Error creating service order: {e}")

        return redirect('/service_order')
    

@login_required
def service_order_update(request, id):
    if request.method == "POST":
        try:
            request_data = json.loads(request.body)

            service_order = Service_Order.objects.get(id=int(id))

            service_order.username = request_data['username']
            service_order.texting = request_data['texting']
            service_order.customer = Customer.objects.get(record_id = int(request_data['customer'])) if request_data['customer'] else None
            service_order.term_location = Term_Location.objects.get(record_id = int(request_data['term_location'])) if request_data['term_location'] else None
            service_order.updated_by = str(request.user)
            service_order.updated_at = datetime.datetime.now()
            service_order.status = 1

            service_order.full_clean()
            service_order.save()

            for item in request_data['number_email_date']:
                if '_' in item['id']:
                    number_email_date_dict = {
                    'number' : int(item['number']),
                    'email' : item['email'],
                    'reseller' : item['reseller'],
                    'requested_port_date' : parse_date(item['requested_port_date']),
                    'e911_number' : int(item['e911_number']) if item['e911_number'] else None,
                    'e911_address' : item['e911_address'],
                    'service_status' : Status.objects.get(record_id=int(item['service_status'])) if item['service_status'] else None,
                    'voice_carrier' : Voice_Carrier.objects.get(record_id=int(item['voice_carrier'])) if item['voice_carrier'] else None,
                    'sms_carrier' : Voice_Carrier.objects.get(record_id=int(item['sms_carrier'])) if item['sms_carrier'] else None,
                    'sms_type' : SMS_Type.objects.get(record_id=int(item['sms_type'])) if item['sms_type'] else None,
                    'sms_enabled' : item['sms_enabled'],
                    'sms_campaign' : item['sms_campaign'],
                    'user_first_name' : item['user_first_name'],
                    'user_last_name' : item['user_last_name'],
                    'extension' : int(item['extension']) if item['extension'] else None,
                    'onboard_date' : parse_date(item['onboard_date']),
                    'e911_enabled_billed' : item['e911_enabled_billed'],
                    'service_1' : Service.objects.get(record_id=int(item['service_1'])) if item['service_1'] else None,
                    'service_2' : Service.objects.get(record_id=int(item['service_2'])) if item['service_2'] else None,
                    'service_3' : Service.objects.get(record_id=int(item['service_3'])) if item['service_3'] else None,
                    'service_4' : Service.objects.get(record_id=int(item['service_4'])) if item['service_4'] else None,
                    }
                    number_email_date = Number_Email_Date.objects.create(**number_email_date_dict)
                    service_order.number_email_dates.add(number_email_date)
                else:
                    service_order_number_email_date_data = Number_Email_Date.objects.get(id=item['id'])
                    service_order_number_email_date_data.number = int(item['number'])
                    service_order_number_email_date_data.email = item['email']
                    service_order_number_email_date_data.reseller = item['reseller']
                    service_order_number_email_date_data.requested_port_date = parse_date(item['requested_port_date']) if item['requested_port_date'] else None
                    service_order_number_email_date_data.e911_number = int(item['e911_number']) if item['e911_number'] else None
                    service_order_number_email_date_data.e911_address = item['e911_address']
                    service_order_number_email_date_data.service_status = Status.objects.get(record_id=item['service_status']) if item['service_status'] else None
                    service_order_number_email_date_data.voice_carrier = Voice_Carrier.objects.get(record_id=item['voice_carrier']) if item['voice_carrier'] else None
                    service_order_number_email_date_data.sms_carrier = Voice_Carrier.objects.get(record_id=item['sms_carrier']) if item['sms_carrier'] else None
                    service_order_number_email_date_data.sms_type = SMS_Type.objects.get(record_id=item['sms_type']) if item['sms_type'] else None
                    service_order_number_email_date_data.sms_enabled = item['sms_enabled']
                    service_order_number_email_date_data.sms_campaign = item['sms_campaign']
                    service_order_number_email_date_data.user_first_name = item['user_first_name']
                    service_order_number_email_date_data.user_last_name = item['user_last_name']
                    service_order_number_email_date_data.extension = int(item['extension']) if item['extension'] else None
                    service_order_number_email_date_data.onboard_date = parse_date(item['onboard_date']) if item['onboard_date'] else None
                    service_order_number_email_date_data.e911_enabled_billed = item['e911_enabled_billed']
                    service_order_number_email_date_data.service_1 = Service.objects.get(record_id=item['service_1']) if item['service_1'] else None
                    service_order_number_email_date_data.service_2 = Service.objects.get(record_id=item['service_2']) if item['service_2'] else None
                    service_order_number_email_date_data.service_3 = Service.objects.get(record_id=item['service_3']) if item['service_3'] else None
                    service_order_number_email_date_data.service_4 = Service.objects.get(record_id=item['service_4']) if item['service_4'] else None

                    service_order_number_email_date_data.save()

            for item in request_data['remove_numbers']:
                remove_item = service_order.number_email_dates.get(id=int(item))
                service_order.number_email_dates.remove(remove_item)
                Number_Email_Date.objects.get(id=int(item)).delete()

            messages.success(request, 'The service order was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/service_order')
    else:
        service_order = Service_Order.objects.get(id=int(id))
        number_email_date = service_order.number_email_dates.all().values()

        customers_data = Customer.objects.values_list('record_id', 'full_name')
        status_data = Status.objects.all()
        voice_carrier_data = Voice_Carrier.objects.all()
        sms_type_data = SMS_Type.objects.all()
        term_location_data = Term_Location.objects.all()
        services_data = Service.objects.all()

        customers = []
        status = []
        voice_carrier = []
        sms_type = []
        term_location = []
        services = []
        number_email_date_data = []

        for item in customers_data:
            if str(item[0]).isdigit():
                customers.append({'id': item[0], 'full_name': item[1]})

        for item in status_data:
            if str(item.record_id).isdigit():
                status.append({'id': item.record_id, 'name': item.name})

        for item in voice_carrier_data:
            if str(item.record_id).isdigit():
                voice_carrier.append({'id': item.record_id, 'name': item.name})

        for item in sms_type_data:
            if str(item.record_id).isdigit():
                sms_type.append({'id': item.record_id, 'name': item.name})

        for item in term_location_data:
            if str(item.record_id).isdigit():
                term_location.append({'id': item.record_id, 'name': item.name})

        for item in services_data:
            if str(item.record_id).isdigit():
                services.append({'id': item.record_id, 'name': item.name})

        service_order_data = {
            'username': service_order.username if service_order.username else '',
            'customer': service_order.customer.record_id if not service_order.customer is None or '' else '',
            'texting': service_order.texting if service_order.texting else '',
            'term_location': service_order.term_location.record_id if not service_order.term_location is None or '' else '',
        }

        for item in number_email_date:
            number_email_date_data.append({
                'id': item['id'],
                'email': item['email'] if item['email'] else '',
                'number': item['number'] if item['number'] else '',
                'requested_port_date': item['requested_port_date'].strftime('%Y-%m-%d') if item['requested_port_date'] else '',
                'e911_number': item['e911_number'] if item['e911_number'] else '',
                'e911_address': item['e911_address'] if item['e911_address'] else '',
                'reseller': item['reseller'] if item['reseller'] else '',
                'service_status': item['service_status_id'] if item['service_status_id'] else '',
                'voice_carrier': item['voice_carrier_id'] if item['voice_carrier_id'] else '',
                'sms_carrier': item['sms_carrier_id'] if item['sms_carrier_id'] else '',
                'sms_type': item['sms_type_id'] if item['sms_type_id'] else '',
                'sms_enabled': item['sms_enabled'] if item['sms_enabled'] else '',
                'sms_campaign': item['sms_campaign'] if item['sms_campaign'] else '',
                'user_first_name': item['user_first_name'] if item['user_first_name'] else '',
                'user_last_name': item['user_last_name'] if item['user_last_name'] else '',
                'extension': item['extension'] if item['extension'] else '',
                'onboard_date': item['onboard_date'].strftime('%Y-%m-%d') if item['onboard_date'] else '',
                'e911_enabled_billed': item['e911_enabled_billed'] if item['e911_enabled_billed'] else '',
                'service_1': item['service_1_id'] if item['service_1_id'] else '',
                'service_2': item['service_2_id'] if item['service_2_id'] else '',
                'service_3': item['service_3_id'] if item['service_3_id'] else '',
                'service_4': item['service_4_id'] if item['service_4_id'] else '',
            })

        return render(request, 'service_order_edit.html', {'service_order': service_order_data, 'number_email_date_data': number_email_date_data, 'customers': customers, 'status': status, 'voice_carriers': voice_carrier, 'sms_carriers': voice_carrier, 'sms_types': sms_type, 'term_locations': term_location, 'services': services})
    

@login_required
def service_order_submit(request, id):
    try:
        service_order = Service_Order.objects.get(id=int(id))
        service_order.status = 2
        service_order.save()

        i = 1

        post_create_msg = pymsteams.connectorcard(os.getenv('TEAMS_WEBHOOK_URL'))
        post_create_msg.title("A new service order was submitted.")
        msg_temp = [f"Here is the detailed information.\n"]
        msg_temp.append(f"- Requested username: {service_order.username}\n" if service_order.username else '')
        msg_temp.append(f"- Requested description: {service_order.texting}\n" if service_order.texting else '')
        msg_temp.append("\n")

        for item in service_order.number_email_dates.all():
            msg_temp.append(f"{i}. Requested number: {item.number}\n" if item.number else '')
            msg_temp.append(f" - Requested email: {item.email}\n" if item.email else '')
            msg_temp.append(f" - Requested port date: {item.requested_port_date}\n" if item.requested_port_date else '')
            msg_temp.append(f" - Requested E911 number: {item.e911_number}\n" if item.e911_number else '')
            msg_temp.append(f" - Requested E911 address: {item.e911_address}\n" if item.e911_address else '')
            i = i + 1

        post_create_msg.text('\n'.join(msg_temp))
        post_create_msg.send()
        
        messages.success(request, 'The service order was submitted successfully!')

    except Exception as e:
        messages.warning(request, e)

    return redirect('/service_order')

@login_required
def service_order_add_step_1(request):
    customers_data = Customer.objects.values_list('record_id', 'full_name')
    status_data = Status.objects.all()
    voice_carrier_data = Voice_Carrier.objects.all()
    sms_type_data = SMS_Type.objects.all()
    term_location_data = Term_Location.objects.all()
    services_data = Service.objects.all()

    customers = []
    status = []
    voice_carrier = []
    sms_type = []
    term_location = []
    services = []

    for item in customers_data:
        if str(item[0]).isdigit():
            customers.append({'id': item[0], 'full_name': item[1]})

    for item in status_data:
        if str(item.record_id).isdigit():
            status.append({'id': item.record_id, 'name': item.name})

    for item in voice_carrier_data:
        if str(item.record_id).isdigit():
            voice_carrier.append({'id': item.record_id, 'name': item.name})

    for item in sms_type_data:
        if str(item.record_id).isdigit():
            sms_type.append({'id': item.record_id, 'name': item.name})

    for item in term_location_data:
        if str(item.record_id).isdigit():
            term_location.append({'id': item.record_id, 'name': item.name})

    for item in services_data:
        if str(item.record_id).isdigit():
            services.append({'id': item.record_id, 'name': item.name})

    if request.method == 'GET':
        return render(request, 'service_order_create_1.html', {'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': voice_carrier, 'sms_type': sms_type, 'term_location': term_location, 'services': services})
    

def service_order_add_step_2(request):
    customers_data = Customer.objects.values_list('record_id', 'full_name')
    status_data = Status.objects.all()
    voice_carrier_data = Voice_Carrier.objects.all()
    sms_type_data = SMS_Type.objects.all()
    term_location_data = Term_Location.objects.all()
    services_data = Service.objects.all()

    customers = []
    status = []
    voice_carrier = []
    sms_type = []
    term_location = []
    services = []

    for item in customers_data:
        if str(item[0]).isdigit():
            customers.append({'id': item[0], 'full_name': item[1]})

    for item in status_data:
        if str(item.record_id).isdigit():
            status.append({'id': item.record_id, 'name': item.name})

    for item in voice_carrier_data:
        if str(item.record_id).isdigit():
            voice_carrier.append({'id': item.record_id, 'name': item.name})

    for item in sms_type_data:
        if str(item.record_id).isdigit():
            sms_type.append({'id': item.record_id, 'name': item.name})

    for item in term_location_data:
        if str(item.record_id).isdigit():
            term_location.append({'id': item.record_id, 'name': item.name})

    for item in services_data:
        if str(item.record_id).isdigit():
            services.append({'id': item.record_id, 'name': item.name})

    if request.method == 'POST':
        context_data = {
                'numbers': [num.strip('\r') for num in request.POST['number'].split('\n') if num.strip('\r')],
                'service_order_name': request.POST['username'],
                'texting': request.POST['texting'],
                'customer': int(request.POST['customer']) if str(request.POST['customer']).isdigit() else '',
                'email': request.POST['email'],
                'requested_port_date': request.POST['requested_port_date'],
                'e911_number': request.POST['e911_number'],
                'e911_address': request.POST['e911_address'],
                'reseller': request.POST['reseller'],
                'term_location': int(request.POST['term_location']) if str(request.POST['term_location']).isdigit() else '',
                'service_status': int(request.POST['status'])  if str(request.POST['status']).isdigit() else '',
                'voice_carrier': int(request.POST['voice_carrier']) if str(request.POST['voice_carrier']).isdigit() else '',
                'sms_carrier': int(request.POST['sms_carrier']) if str(request.POST['sms_carrier']).isdigit() else '',
                'sms_type': int(request.POST['sms_type']) if str(request.POST['sms_type']).isdigit() else '',
                'sms_enabled': request.POST['sms_enabled'],
                'sms_campaign': request.POST['sms_campaign'],
                'user_first_name': request.POST['user_first_name'],
                'user_last_name': request.POST['user_last_name'],
                'extension': request.POST['extension'],
                'onboard_date': request.POST['onboard_date'],
                'e911_enabled_billed': request.POST['e911_enabled_billed'],
                'service_1': int(request.POST['service_1']) if str(request.POST['service_1']).isdigit() else '',
                'service_2': int(request.POST['service_2']) if str(request.POST['service_2']).isdigit() else '',
                'service_3': int(request.POST['service_3']) if str(request.POST['service_3']).isdigit() else '',
                'service_4': int(request.POST['service_4']) if str(request.POST['service_4']).isdigit() else '',
                'customers': customers,
                'status': status,
                'voice_carriers': voice_carrier,
                'sms_carriers': voice_carrier,
                'sms_types': sms_type,
                'term_locations': term_location,
                'services': services
            }
        
        return render(request, 'service_order_create_2.html', context_data)
    else:
        return redirect('/service_order')
        