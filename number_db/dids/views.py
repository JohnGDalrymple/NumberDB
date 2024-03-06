from django.shortcuts import render, redirect
import csv
from .models import *
from django.db.models import Q
from customers.models import *
from assist_dids.models import *
import datetime
from functools import reduce
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
import uuid
from operator import or_
import requests
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from dateutil import parser
import json

email_regex = r"(^[a-zA-Z0-9_.+\-']+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def is_valid_email(email):
    if email == None or email == '':
        return ''
    elif ',' in email:
        return email
    elif(re.search(email_regex, email.strip())):  
        return email  
    else:  
        return email + '@outlook.com'


default_data_header = ['did', 'customer', 'reseller', 'in_method', 'status', 'change_date', 'voice_carrier', 'sms_enabled', 'sms_carrier', 'sms_type', 'sms_campaign', 'term_location', 'user_first_name', 'user_last_name', 'extension', 'email', 'onboard_date', 'note', 'e911_enabled_billed', 'e911_cid', 'e911_address', 'did_uuid', 'service_1', 'service_2', 'service_3', 'service_4', 'updated_date_time', 'updated_by']

default_header = ['DID', 'Customer', 'Reseller', 'In Method', 'Status', 'Change Date', 'Voice Carrier', 'SMS Enabled', 'SMS Carrier', 'SMS Type', 'SMS Campaign', 'Term Location', 'User First Name', 'User Last Name', 'Extension', 'Email', 'Onboard Date', 'Note', 'E911 Enabled Billed', 'E911 CID', 'E911 Address', 'DID uuid', 'Service 1', 'Service 2', 'Service 3', 'Service 4', 'Updated Date Time', 'Updated By']


def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y').date() if date_string else None


def parse_datetime(datetime_string):
    try:
        return datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S').date()
    except ValueError:
        return datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S').date() if datetime_string else None
   

def parse_date_sync(date_string):
    if date_string:
        if '.' in date_string:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
        else:
            date_format = "%Y-%m-%dT%H:%M:%S"

        return datetime.datetime.strptime(date_string, date_format).date()
    else:
        return None

def parse_datetime_sync(date_string):
    if date_string:
        if '.' in date_string:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
        else:
            date_format = "%Y-%m-%dT%H:%M:%S"

        return datetime.datetime.strptime(date_string, date_format).date()
    else:
        return None


def switch(value):
    if value.lower() == "yes":
        return "Yes"
    elif value.lower() == "no":
        return "No"
    return ""


def check_customer(customer_name):
    try:
        customer = Customer.objects.get(full_name__iexact = customer_name)
        return customer
    except Exception as e:
        return True if customer_name else None


def check_service_status(status_value):
    try:
        service_status = Status.objects.get(name__iexact = status_value)
        return service_status
    except Exception as e:
        return True if status_value else None


def check_voice_sms_carrier(carrier_value):
    try:
        voice_carrier = Voice_Carrier.objects.get(name__iexact = carrier_value)
        return voice_carrier
    except Exception as e:
        return True if carrier_value else None
    

def check_sms_type(sms_type_value):
    try:
        sms_type = SMS_Type.objects.get(name__iexact = sms_type_value)
        return sms_type
    except Exception as e:
        return True if sms_type_value else None
    

def check_term_location(term_location_value):
    try:
        term_location = Term_Location.objects.get(name__iexact = term_location_value)
        return term_location
    except Exception as e:
        return True if term_location_value else None


def check_service_item(service_item_value):
    try:
        service_item = Service.objects.get(name__iexact = service_item_value)
        return service_item
    except Exception as e:
        return True if service_item_value else None
    

def is_date(date_value):
    if date_value:
        try:
            dt = parser.parse(date_value)
            formatted_date = dt.strftime('%Y-%m-%d')
            # datetime.datetime.strptime(date_value, "%Y-%m-%d")
            return False
        except Exception:
            return True
    else: return False


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def did(request):
    if request.method == 'GET':
        did_error = Did_Error.objects.all().values()
        dids_list = []
        if request.GET.get('search'):
            query = request.GET['search']

            # dids_list = Did.objects.filter(q_objects).distinct().values()
            q_objects = []
            q_objects.append((Q(did__icontains = query)))
            q_objects.append((Q(reseller__icontains = query)))
            q_objects.append((Q(user_first_name__icontains = query)))
            q_objects.append((Q(user_last_name__icontains = query)))
            q_objects.append((Q(email__icontains = query)))
            q_objects.append((Q(onboard_date__contains = query)))
            q_objects.append((Q(note__icontains = query)))
            q_objects.append((Q(in_method__icontains = query)))
            q_objects.append((Q(sms_campaign__icontains = query)))
            q_objects.append((Q(sms_enabled__icontains = query)))
            q_objects.append((Q(extension__icontains = query)))
            q_objects.append((Q(e911_enabled_billed__icontains = query)))
            q_objects.append((Q(e911_cid__icontains = query)))
            q_objects.append((Q(e911_address__icontains = query)))
            q_objects.append((Q(updated_by__icontains = query)))
            
            # Add Q objects for foreign key fields
            q_objects.append((Q(status__name__icontains = query)))
            q_objects.append((Q(voice_carrier__name__icontains = query)))
            q_objects.append((Q(sms_carrier__name__icontains = query)))
            q_objects.append((Q(sms_type__name__icontains = query)))
            q_objects.append((Q(term_location__name__icontains = query)))
            q_objects.append((Q(customer__full_name__icontains = query)))
            q_objects.append((Q(service_1__name__icontains = query)))
            q_objects.append((Q(service_2__name__icontains = query)))
            q_objects.append((Q(service_3__name__icontains = query)))
            q_objects.append((Q(service_4__name__icontains = query)))
            
            # Use Q object to query the database with OR condition
            dids_list = Did.objects.filter(reduce(or_, q_objects))

            for item in dids_list:
                item.note =  "" if(item.note == None) else item.note
                item.e911_enabled_billed =  "" if(item.e911_enabled_billed == None) else item.e911_enabled_billed
                item.e911_address =  "" if(item.e911_address == None) else item.e911_address
                item.updated_by =  "" if(item.updated_by == None) else item.updated_by
                item.change_date =  "" if(item.change_date == None) else item.change_date
                item.extension =  "" if(item.extension == None) else item.extension
                item.onboard_date =  "" if(item.onboard_date == None) else item.onboard_date
                item.e911_cid =  "" if(item.e911_cid == None) else item.e911_cid
                item.updated_date_time =  "" if(item.updated_date_time == None) else item.updated_date_time
            
            size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(dids_list, size)
            dids = paginator.get_page(page_number)
                
            return render(request, 'dids.html', {'dids': dids, 'search': query, 'error': did_error})

        else:
            dids_list = Did.objects.all().select_related('customer', 'status', 'voice_carrier', 'sms_carrier', 'sms_type', 'term_location', 'service_1', 'service_2', 'service_3', 'service_4')
            for item in dids_list:
                item.note =  "" if(item.note == None) else item.note
                item.e911_enabled_billed =  "" if(item.e911_enabled_billed == None) else item.e911_enabled_billed
                item.e911_address =  "" if(item.e911_address == None) else item.e911_address
                item.updated_by =  "" if(item.updated_by == None) else item.updated_by
                item.change_date =  "" if(item.change_date == None) else item.change_date
                item.extension =  "" if(item.extension == None) else item.extension
                item.onboard_date =  "" if(item.onboard_date == None) else item.onboard_date
                item.e911_cid =  "" if(item.e911_cid == None) else item.e911_cid
                item.updated_date_time =  "" if(item.updated_date_time == None) else item.updated_date_time
            
            size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(dids_list, size)
            dids = paginator.get_page(page_number)
                    
            return render(request, 'dids.html', {'dids': dids, 'error': did_error})
    
    if request.method == 'POST':
            try:
                if request.FILES:
                    csv_file = request.FILES["csv_file"]

                    if len(csv_file) == 0:
                        messages.warning(request, 'Empty File')

                    if not csv_file.name.endswith('.csv'):
                        messages.warning(request, 'File is not CSV type')

                    if csv_file.multiple_chunks():
                        messages.warning(request, 'Uploaded file is too big (%.2f MB).' % (csv_file.size / (1000 * 1000),))

                    data_df = pd.read_csv(csv_file, dtype=str)
                    data_dict = data_df.to_dict('records')
                    
                    if data_dict != []:
                        if set(data_dict[0].keys()) == set(default_header):
                            convert_data = data_df.fillna('')
                            convert_data = convert_data.to_dict('records')

                            error_flag = False

                            for item in convert_data:
                                customer_value = check_customer(item['Customer'])
                                service_status_value = check_service_status(item['Status'])
                                voice_carrier_value = check_voice_sms_carrier(item['Voice Carrier'])
                                sms_carrier_value = check_voice_sms_carrier(item['SMS Carrier'])
                                sms_type_value = check_sms_type(item['SMS Type'])
                                term_location_value = check_term_location(item['Term Location'])
                                service_item_1 = check_service_item(item['Service 1'])
                                service_item_2 = check_service_item(item['Service 2'])
                                service_item_3 = check_service_item(item['Service 3'])
                                service_item_4 = check_service_item(item['Service 4'])
                                # print(item['DID'], item['Change Date'], is_date(item['Change Date']), item['Updated Date Time'], is_date(item['Updated Date Time']), item['Onboard Date'], is_date(item['Onboard Date']))

                                if (not item['DID'].isdigit()) or (switch(item['In Method']) == True) or (voice_carrier_value == True) or (service_status_value == True) or (switch(item['SMS Enabled']) == True) or (sms_carrier_value == True) or (sms_type_value == True) or (term_location_value == True) or (switch(item['E911 Enabled Billed']) == True) or (customer_value == True) or (service_item_1 == True) or (service_item_2 == True) or (service_item_3 == True) or (service_item_4 == True) or not ( not item['Extension'] or item['Extension'].isdigit()) or not ( not item['E911 CID'] or item['E911 CID'].isdigit()) or is_date(item['Change Date']) or is_date(item['Updated Date Time']) or is_date(item['Onboard Date']):
                                    error_flag = True
                                    save_data = Did_Error(
                                    # did_uuid = item['DID uuid'], 
                                    did_uuid = uuid.uuid4(), 
                                    did = item['DID'], 
                                    in_method = item['In Method'], 
                                    voice_carrier = item['Voice Carrier'], 
                                    status = item['Status'], 
                                    change_date = item['Change Date'], 
                                    sms_enabled = item['SMS Enabled'], 
                                    sms_carrier = item['SMS Carrier'], 
                                    sms_type = item['SMS Type'], 
                                    sms_campaign = item['SMS Campaign'], 
                                    term_location = item['Term Location'], 
                                    customer = item['Customer'], 
                                    reseller = item['Reseller'], 
                                    user_first_name = item['User First Name'], 
                                    user_last_name = item['User Last Name'], 
                                    extension = item['Extension'],
                                    email = item['Email'], 
                                    onboard_date = item['Onboard Date'], 
                                    note = item['Note'], 
                                    e911_enabled_billed = item['E911 Enabled Billed'], 
                                    e911_cid = item['E911 CID'],
                                    e911_address = item['E911 Address'], 
                                    service_1 = item['Service 1'], 
                                    service_2 = item['Service 2'], 
                                    service_3 = item['Service 3'], 
                                    service_4 = item['Service 4'], 
                                    updated_date_time = item['Updated Date Time'], 
                                    updated_by = item['Updated By'], 
                                    )
                                    try:
                                        save_data.save()
                                        print("Error saved!")
                                    except Exception as e:
                                        messages.warning(request, e)
                                else:
                                    try:
                                        try:
                                            find_one = Did.objects.get(did = int(item['DID']))
                                            find_one.did_uuid = item['DID uuid'] if item['DID uuid'] else uuid.uuid4()
                                            find_one.did = item['DID'] if item['DID'] else None
                                            find_one.in_method = switch(item['In Method'])
                                            find_one.voice_carrier = voice_carrier_value
                                            find_one.status = service_status_value
                                            find_one.change_date =  datetime.datetime.now()
                                            find_one.sms_enabled = switch(item['SMS Enabled'])
                                            find_one.sms_carrier = sms_carrier_value
                                            find_one.sms_type = sms_type_value
                                            find_one.sms_campaign = item['SMS Campaign']
                                            find_one.term_location = term_location_value
                                            find_one.customer = customer_value
                                            find_one.reseller = item['Reseller']
                                            find_one.user_first_name = item['User First Name']
                                            find_one.user_last_name = item['User Last Name']
                                            find_one.extension = item['Extension'] if item['Extension'] else None
                                            find_one.email = item['Email']
                                            find_one.onboard_date = parse_date(item['Onboard Date'])
                                            find_one.note = item['Note']
                                            find_one.e911_enabled_billed = switch(item['E911 Enabled Billed'])
                                            find_one.e911_cid = item['E911 CID'] if item['E911 CID'] else None
                                            find_one.e911_address = item['E911 Address']
                                            find_one.service_1 = service_item_1
                                            find_one.service_2 = service_item_2
                                            find_one.service_3 = service_item_3
                                            find_one.service_4 = service_item_4
                                            find_one.updated_date_time = datetime.datetime.now()
                                            find_one.updated_by = item['Updated By']
                                            find_one.is_synced = True if item['In Method'] == "Yes" else False
                                            find_one.full_clean()
                                            find_one.save()
                                        except Exception:
                                            save_data = Did(
                                            # did_uuid = item['DID uuid'] if item['DID uuid'] else uuid.uuid4(), 
                                            did_uuid = uuid.uuid4(), 
                                            did = item['DID'] if item['DID'] else None, 
                                            in_method = switch(item['In Method']), 
                                            voice_carrier = voice_carrier_value, 
                                            status = service_status_value, 
                                            change_date =  datetime.datetime.now(), 
                                            sms_enabled = switch(item['SMS Enabled']), 
                                            sms_carrier = sms_carrier_value, 
                                            sms_type = sms_type_value, 
                                            sms_campaign = item['SMS Campaign'], 
                                            term_location = term_location_value, 
                                            customer = customer_value, 
                                            reseller = item['Reseller'], 
                                            user_first_name = item['User First Name'], 
                                            user_last_name = item['User Last Name'], 
                                            extension = item['Extension'] if item['Extension'] else None,
                                            email = item['Email'], 
                                            onboard_date = parse_date(item['Onboard Date']), 
                                            note = item['Note'], 
                                            e911_enabled_billed = switch(item['E911 Enabled Billed']), 
                                            e911_cid = item['E911 CID'] if item['E911 CID'] else None, 
                                            e911_address = item['E911 Address'], 
                                            service_1 = service_item_1, 
                                            service_2 = service_item_2, 
                                            service_3 = service_item_3, 
                                            service_4 = service_item_4, 
                                            updated_date_time = datetime.datetime.now(),
                                            updated_by = item['Updated By'], 
                                            is_synced = False,
                                            )
                                            save_data.save()
                                            print("Success saved!")
                                    except Exception as e:
                                        print(e)
                                        messages.warning(request, e)
                            if error_flag:
                                messages.warning(request, "There are uncorrect fields in the CSV file, Please check it and upload again.")
                            messages.success(request, "Successfully Uploaded CSV File and Added to database")
                            
                        else:
                            messages.warning(request, "This file format is not correct. Please download `Sample CSV` and wirte the doc as it")
                    else: 
                        messages.warning(request, "This file is empty!")
                else:
                    messages.warning(request, "Please upload CSV file.")
            except Exception as e:
                messages.warning(request, "Unable to upload file." + e)
    return redirect('/did')


@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})


@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.warning(request, 'User was deleted successfully!')
    return redirect('/user')


@login_required
def user_edit(request, id):
    user = User.objects.filter(id=id).values()[0]
    userData = {
        'id': user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'username': user['username'],
        'email': user['email'],
        'date_joined': user['date_joined'].strftime('%Y-%m-%d'),
    }
    context = {'user': userData}
    return render(request, 'user_edit.html', context)


@login_required
def user_add(request):
    if request.method == "POST":
        try:
            users = User(
                username = request.POST['username'],
                password = make_password(request.POST['password1']),
                is_staff = True,
                is_active = True,
                is_superuser = True,
                email = request.POST['email'],
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
            )
            users.full_clean()
            users.save()
            s = smtplib.SMTP(os.getenv('SMTP_SERVICE'), os.getenv('EMAIL_PORT'))
            s.starttls()
            s.login(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PASSWORD'))

            client_message_html = f"""\
            <html>
                <body>
                    <p style="font-size:16px">Hello <strong>{request.POST['first_name']}</strong>.</p>
                    <br>
                    <p><strong>Congratulations🎉,</strong> You have been invited to become an administrator of the Mobex server.</p>
                    <p>You can access <a href="{os.getenv('BASE_URL')}" style="text-decoration:none"><strong>Mobex admin panel</strong></a> using below credential</p>
                    <p>Username: <strong>{request.POST['username']}</strong></p>
                    <p>Password: <strong>{request.POST['password1']}</strong></p>
                    <br>
                    <p>Thank you.</p>
                    <p style="font-size:16px"><strong>Mobex.</strong></p>
                </body>
            </html>
            """

            client_message = MIMEMultipart('alternative')
            client_message.attach(MIMEText(client_message_html, _subtype='html'))
            
            client_message["Subject"] = 'Welcome to Mobex!'
            client_message["From"] = os.getenv('EMAIL_SERVER')
            client_message["To"] = request.POST['email']

            s.sendmail(os.getenv('EMAIL_SERVER'), request.POST['email'], client_message.as_string())
            s.quit()

        except Exception as e:
            messages.warning(request, e)

        messages.success(request, 'User was created successfully!')
        return HttpResponseRedirect('/user')
    
    else:
        return render(request, 'user_create.html')


@login_required
def user_update(request, id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.date_joined = request.POST['date_joined']
            user.save()
            messages.success(request, 'User was updated successfully!')

        except Exception as e:
            messages.warning(request, e)

        return redirect('/user')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password1']),
                is_staff=True,
                is_active=True,
                is_superuser=True,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            try:
                user.full_clean()
            except ValidationError as e:
                pass
            user.save()
            messages.success(request, 'Member was created successfully!')
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def register_success(request):
    return render(request, 'success.html')


@login_required
def did_add(request):
    if request.method == 'POST':
        try:
            did = Did(
                did = int(request.POST['did']) if request.POST['did'].isdigit() else None,
                customer = Customer.objects.get(record_id = int(request.POST['customer'])) if request.POST['customer'] else None,
                reseller = request.POST['reseller'],
                in_method = request.POST['in_method'],
                status = Status.objects.get(record_id = int(request.POST['status'])) if request.POST['status'] else None,
                change_date = parse_date(request.POST['change_date']),
                voice_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['voice_carrier'])) if request.POST['voice_carrier'] else None,
                sms_enabled = request.POST['sms_enabled'],
                sms_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['sms_carrier'])) if request.POST['sms_carrier'] else None,
                sms_type = SMS_Type.objects.get(record_id = int(request.POST['sms_type'])) if request.POST['sms_type'] else None,
                sms_campaign = request.POST['sms_campaign'],
                term_location = Term_Location.objects.get(record_id = int(request.POST['term_location'])) if request.POST['term_location'] else None,
                user_first_name = request.POST['user_first_name'],
                user_last_name = request.POST['user_last_name'],
                extension = int(request.POST['extension']) if request.POST['extension'].isdigit() else None,
                email = is_valid_email(request.POST['email']),
                onboard_date = parse_date(request.POST['onboard_date']),
                note = request.POST['note'],
                e911_enabled_billed = request.POST['e911_enabled_billed'],
                e911_cid = int(request.POST['e911_cid']) if request.POST['e911_cid'].isdigit() else None,
                e911_address = request.POST['e911_address'],
                did_uuid = uuid.uuid4(),
                service_1 = Service.objects.get(record_id = int(request.POST['service_1'])) if request.POST['service_1'] else None,
                service_2 = Service.objects.get(record_id = int(request.POST['service_2'])) if request.POST['service_2'] else None,
                service_3 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None,
                service_4 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None,
                updated_date_time = datetime.datetime.now(),
                updated_by = request.user,
                )
            
            did.full_clean()
            did.save()

            messages.success(request, 'DID was created successfully!')
        
        except Exception as e:
            messages.warning(request, e)

        return redirect('/did')
    else:
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

        return render(request, 'did_create.html', {'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': voice_carrier, 'sms_type': sms_type, 'term_location': term_location, 'services': services})
    

@login_required
def did_delete(request, id):
    try:
        did = Did.objects.get(id=id)
        did.is_active = False
        did.save()
        messages.warning(request, 'DID was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)

    return redirect('/did')


@login_required
def did_edit(request, id):
    did = Did.objects.filter(id=id).values()[0]
    didData = {
        'id': did['id'],
        'did': did['did'],
        'customer': did['customer_id'],
        'reseller': did['reseller'],
        'in_method': did['in_method'],
        'status': did['status_id'],
        'change_date': did['change_date'] if not did['change_date'] else did['change_date'].strftime('%Y-%m-%d'),
        'voice_carrier': did['voice_carrier_id'],
        'sms_enabled': did['sms_enabled'],
        'sms_carrier': did['sms_carrier_id'],
        'sms_type': did['sms_type_id'],
        'sms_campaign': did['sms_campaign'],
        'term_location': did['term_location_id'],
        'user_first_name': did['user_first_name'],
        'user_last_name': did['user_last_name'],
        'extension': did['extension'],
        'email': did['email'],
        'onboard_date': did['onboard_date'] if not did['onboard_date'] else did['onboard_date'].strftime('%Y-%m-%d'),
        'note': did['note'],
        'e911_enabled_billed': did['e911_enabled_billed'],
        'e911_cid': did['e911_cid'],
        'e911_address': did['e911_address'],
        'did_uuid': did['did_uuid'],
        'service_1': did['service_1_id'],
        'service_2': did['service_2_id'],
        'service_3': did['service_3_id'],
        'service_4': did['service_4_id'],
        'updated_date_time': did['updated_date_time'] if not did['updated_date_time'] else did['updated_date_time'].strftime('%Y-%m-%d'),
        'updated_by': did['updated_by'],
    }

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

    return render(request, 'did_edit.html', {'did': didData, 'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': voice_carrier, 'sms_type': sms_type, 'term_location': term_location, 'services': services})


@login_required
def did_update(request, id):
    did = Did.objects.get(id=id)
    if request.method == "POST":
        try:
            did.did = int(request.POST['did']) if request.POST['did'].isdigit() else None
            did.customer = Customer.objects.get(record_id = int(request.POST['customer'])) if request.POST['customer'] else None
            did.reseller = request.POST['reseller']
            did.in_method = request.POST['in_method']
            did.status = Status.objects.get(record_id = int(request.POST['status'])) if request.POST['status'] else None
            did.change_date = parse_date(request.POST['change_date'])
            did.voice_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['voice_carrier'])) if request.POST['voice_carrier'] else None
            did.sms_enabled = request.POST['sms_enabled']
            did.sms_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['sms_carrier'])) if request.POST['sms_carrier'] else None
            did.sms_type = SMS_Type.objects.get(record_id = int(request.POST['sms_type'])) if request.POST['sms_type'] else None
            did.sms_campaign = request.POST['sms_campaign']
            did.term_location = Term_Location.objects.get(record_id = int(request.POST['term_location'])) if request.POST['term_location'] else None
            did.user_first_name = request.POST['user_first_name']
            did.user_last_name = request.POST['user_last_name']
            did.extension = int(request.POST['extension']) if request.POST['extension'].isdigit() else None
            did.email = is_valid_email(request.POST['email'])
            did.onboard_date = parse_date(request.POST['onboard_date'])
            did.note = request.POST['note']
            did.e911_enabled_billed = request.POST['e911_enabled_billed']
            did.e911_cid = int(request.POST['e911_cid']) if request.POST['e911_cid'].isdigit() else None
            did.e911_address = request.POST['e911_address']
            did.did_uuid = uuid.uuid4()
            did.service_1 = Service.objects.get(record_id = int(request.POST['service_1'])) if request.POST['service_1'] else None
            did.service_2 = Service.objects.get(record_id = int(request.POST['service_2'])) if request.POST['service_2'] else None
            did.service_3 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None
            did.service_4 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None
            did.updated_date_time = datetime.datetime.now()
            did.updated_by = request.user.username
            did.is_synced = False
            did.save()
            messages.success(request, 'DID was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/did')
    

@login_required
def export_csv(request):
    ids = request.GET.get('pk')
    
    if (ids):
        id_array = ids.split(",")
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CurrentStatus.csv"'
        writer = csv.writer(response)
        writer.writerow(default_header)

        for id in id_array:
            data = Did.objects.get(id = int(id))
            writer.writerow([
                data.did,
                data.customer if data.customer == None else data.customer.full_name,
                data.reseller,
                data.in_method,
                data.status if data.status == None else data.status.name, 
                data.change_date,
                data.voice_carrier if data.voice_carrier == None else data.voice_carrier.name,
                data.sms_enabled,
                data.sms_carrier if data.sms_carrier == None  else data.sms_carrier.name,
                data.sms_type if data.sms_type == None  else data.sms_type.name,
                data.sms_campaign,
                data.term_location if data.term_location == None  else data.term_location.name,
                data.user_first_name,
                data.user_last_name,
                data.extension,
                data.email,
                data.onboard_date,
                data.note,
                data.e911_enabled_billed,
                data.e911_cid,
                data.e911_address,
                data.did_uuid,
                data.service_1 if data.service_1 == None  else data.service_1.name,
                data.service_2 if data.service_2 == None  else data.service_2.name,
                data.service_3 if data.service_3 == None  else data.service_3.name,
                data.service_4 if data.service_4 == None  else data.service_4.name,
                data.updated_date_time,
                data.updated_by,
                ])

        return response

    else:
        messages.warning(request, 'Please slect in this table')
        return redirect('/did')


@login_required
def did_download_all(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CurrentDID.csv"'
    writer = csv.writer(response)
    writer.writerow(default_header)

    data = Did.objects.all()
    for item in data:
        writer.writerow([
            item.did,
            item.customer if item.customer == None else item.customer.full_name,
            item.reseller,
            item.in_method,
            item.status if item.status == None else item.status.name, 
            item.change_date,
            item.voice_carrier if item.voice_carrier == None else item.voice_carrier.name,
            item.sms_enabled,
            item.sms_carrier if item.sms_carrier == None  else item.sms_carrier.name,
            item.sms_type if item.sms_type == None  else item.sms_type.name,
            item.sms_campaign,
            item.term_location if item.term_location == None  else item.term_location.name,
            item.user_first_name,
            item.user_last_name,
            item.extension,
            item.email,
            item.onboard_date,
            item.note,
            item.e911_enabled_billed,
            item.e911_cid,
            item.e911_address,
            item.did_uuid,
            item.service_1 if item.service_1 == None  else item.service_1.name,
            item.service_2 if item.service_2 == None  else item.service_2.name,
            item.service_3 if item.service_3 == None  else item.service_3.name,
            item.service_4 if item.service_4 == None  else item.service_4.name,
            item.updated_date_time,
            item.updated_by,
            ])

    return response


@login_required
def export_error_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ErrorReport.csv"'
    writer = csv.writer(response)
    writer.writerow(default_header)

    error_data = Did_Error.objects.all()
    
    for item in error_data:
        writer.writerow([
            item.did,
            item.customer,
            item.reseller,
            item.in_method,
            item.status,
            item.change_date,
            item.voice_carrier,
            item.sms_enabled,
            item.sms_carrier,
            item.sms_type,
            item.sms_campaign,
            item.term_location,
            item.user_first_name,
            item.user_last_name,
            item.extension,
            item.email,
            item.onboard_date,
            item.note,
            item.e911_enabled_billed,
            item.e911_cid,
            item.e911_address,
            item.did_uuid,
            item.service_1,
            item.service_2,
            item.service_3,
            item.service_4,
            item.updated_date_time,
            item.updated_by,
            ])
        
    return response


@login_required
def did_sync_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'Number,MIEntityFullName_RecordID,MIResellerMSP,MISMSType_RecordID,MISMSCarrier_RecordID,MISMSCarrier_RecordID,MITermLocation_RecordID,IsDuplicated,LastModifiedDate,MISMSEnabled,MISMSCampaign,MIUserFirstName,MIUserLastName,MIExtension,MIEmail,MIStartDate,MIItemFullName_RecordID,MIItemFullName2_RecordID,MIItemFullName3_RecordID,MIItemFullName4_RecordID,LastModifiedDate,ImportBy,RecordID,MIType_RecordID'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}MICustomerNumberRelationshipTable", headers=headers, params=params)

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
            save_data = Did(
                did = item["Number"],
                customer_id = item["MIEntityFullName_RecordID"],
                reseller = item["MIResellerMSP"],
                status_id = item["MIType_RecordID"],
                voice_carrier_id = item["MISMSCarrier_RecordID"],
                sms_carrier_id = item["MISMSCarrier_RecordID"],
                sms_type_id = item["MISMSType_RecordID"],
                term_location_id = item["MITermLocation_RecordID"],
                in_method = "Yes",
                change_date = parse_date_sync(item["LastModifiedDate"]),
                sms_enabled = "Yes" if item["MISMSEnabled"] else "No",
                sms_campaign = item["MISMSCampaign"],
                user_first_name = item["MIUserFirstName"],
                user_last_name = item["MIUserLastName"],
                extension = item["MIExtension"],
                email = is_valid_email(item["MIEmail"]),
                onboard_date = parse_date_sync(item["MIStartDate"]),
                service_1_id = item["MIItemFullName_RecordID"],
                service_2_id = item["MIItemFullName2_RecordID"],
                service_3_id = item["MIItemFullName3_RecordID"],
                service_4_id = item["MIItemFullName4_RecordID"],
                updated_date_time = parse_date_sync(item["LastModifiedDate"]),
                updated_by = item["ImportBy"],
                record_id = item["RecordID"],
                did_uuid = uuid.uuid4(),
                is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "DID data has been synchronized with Method.")
    return redirect('/did')


def user_verify(request):
    if request.method == "GET":
        return render(request, 'verify.html')
    else:
        try:
            user = User.objects.get(username = request.POST["username"])

            payload = {
                "user_id": user.id,
                "username": user.username,
            }

            expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            payload["exp"] = expiration
            token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

            s = smtplib.SMTP(os.getenv('SMTP_SERVICE'), os.getenv('EMAIL_PORT'))
            s.starttls()
            s.login(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PASSWORD'))

            verify_message_html = f"""\
            <html>
                <body>
                    <p style="font-size:16px">Hello <strong>{user.username}</strong>.</p>
                    <br>
                    <p><strong>Mobex Server</strong> had verified your account, so you can reset your password using <a href="http://localhost:8000/reset/password/?verify={token}" style="text-decoration:none"><strong>here link</strong></a> in three hours</p>
                    <p>After reseting your password, you can access <a href="http://localhost:8000/" style="text-decoration:none"><strong>here</strong></a> using new password</p>
                    <br>
                    <p>Thank you.</p>
                    <p style="font-size:16px"><strong>Mobex.</strong></p>
                </body>
            </html>
            """

            verify_message = MIMEMultipart('alternative')
            verify_message.attach(MIMEText(verify_message_html, _subtype='html'))
            
            verify_message["Subject"] = 'Verify User'
            verify_message["From"] = os.getenv('EMAIL_SERVER')
            verify_message["To"] = user.email

            s.sendmail(os.getenv('EMAIL_SERVER'), user.email, verify_message.as_string())
            s.quit()
            messages.success(request, f"Please check your email inbox({user.email}).")
        except Exception as e:
            messages.warning(request, e)
        return redirect('/user/verify')


def reset_password(request):
    if request.GET.get('verify'):
        try:
            decoded_data = jwt.decode(request.GET.get('verify'), os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            if request.method == 'GET':
                return render(request, 'reset_password.html')
            else:
                if ( not request.POST['password1'] == request.POST['password2']):
                    messages.warning(request, "The password is not match, please check confirm password.")
                else:
                    try:
                        user = User.objects.get(id=decoded_data['user_id'])
                        user.password = make_password(request.POST['password2'])
                        user.save()
                        return render(request, 'reset_password_success.html')
                    except Exception as e:
                        messages.warning(request, e)
                return redirect(f"/reset/password/?verify={request.GET.get('verify')}")
        except jwt.ExpiredSignatureError:
            return redirect('/')
        except jwt.InvalidTokenError:
            return redirect('/')


@login_required
def did_standardization(request):
    did_error = None
    
    convert_did_error = []

    if request.GET.get('search'):
        query = request.GET['search']
        q_objects = Q()
        for field in default_data_header:
            q_objects |= Q(**{field + '__icontains': query})

        did_error = Did_Error.objects.filter(q_objects)
    else:
        did_error = Did_Error.objects.all()
        
    size = request.GET.get('size', 10)
    page_number = request.GET.get('page')
    paginator = Paginator(did_error, size)
    dids_error_list = paginator.get_page(page_number)

    for item in dids_error_list:
        convert_did_error.append({
            'id': item.id,
            'did': item.did,
            'did_status': item.did.isdigit(),
            'customer': item.customer,
            'customer_status': False if check_customer(item.customer) == True else True,
            'reseller': item.reseller,
            'in_method': item.in_method,
            'in_method_status': True if item.in_method == None or item.in_method.lower() == 'yes' or item.in_method.lower() == 'no' or item.in_method == '' else False,
            'status': item.status,
            'status_status': False if check_service_status(item.status) == True else True,
            'voice_carrier': item.voice_carrier,
            'voice_carrier_status': False if check_voice_sms_carrier(item.voice_carrier) == True else True,
            'sms_carrier': item.sms_carrier,
            'sms_carrier_status': False if check_voice_sms_carrier(item.sms_carrier) == True else True,
            'sms_enabled': item.sms_enabled,
            'sms_enabled_status': True if item.sms_enabled == None or item.sms_enabled.lower() == 'yes' or item.sms_enabled.lower() == 'no' or item.sms_enabled == '' else False,
            'sms_type': item.sms_type,
            'sms_type_status': False if check_sms_type(item.sms_type) == True else True,
            'sms_campaign': item.sms_campaign,
            'term_location': item.term_location,
            'term_location_status': False if check_term_location(item.term_location) == True else True,
            'user_first_name': item.user_first_name,
            'user_last_name': item.user_last_name,
            'extension': item.extension,
            'extension_status': item.extension.isdigit() if item.extension else True,
            'email': item.email,
            'email_status': True if item.email == None or item.email == '' else True if re.search(email_regex, item.email.strip()) else False,
            'onboard_date': item.onboard_date,
            'onboard_date_status': not is_date(item.onboard_date),
            'note': item.note,
            'e911_enabled_billed': item.e911_enabled_billed,
            'e911_enabled_billed_status': True if item.e911_enabled_billed == None or item.e911_enabled_billed.lower() == 'yes' or item.e911_enabled_billed.lower() == 'no' or item.e911_enabled_billed == '' else False,
            'e911_cid': item.e911_cid,
            'e911_cid_status': item.e911_cid.isdigit() if item.e911_cid else True,
            'e911_address': item.e911_address,
            'service_1': item.service_1,
            'service_1_status': False if check_service_item(item.service_1) == True else True,
            'service_2': item.service_2,
            'service_2_status': False if check_service_item(item.service_2) == True else True,
            'service_3': item.service_3,
            'service_3_status': False if check_service_item(item.service_3) == True else True,
            'service_4': item.service_4,
            'service_4_status': False if check_service_item(item.service_4) == True else True,
            'updated_by': item.updated_by,
        })

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

    convert_data = {
        'did': convert_did_error,
        'has_next': dids_error_list.has_next(),
        'has_previous': dids_error_list.has_previous(),
        'number': dids_error_list.number,
        'paginator': dids_error_list.paginator,
        'next_page_number': dids_error_list.next_page_number() if dids_error_list.has_next() else None,
        'previous_page_number': dids_error_list.previous_page_number() if dids_error_list.has_previous() else None,
        'customers': customers,
        'status': status,
        'voice_carrier': voice_carrier,
        'sms_carrier': voice_carrier,
        'sms_type': sms_type,
        'term_location': term_location,
        'services': services
    }

    return render(request, 'dids_standardization.html', {'dids_error_list': convert_data})


@login_required
def did_standardization_delete(request, id):
    did_error = Did_Error.objects.get(id=id)
    did_error.delete()
    messages.success(request, 'The Non-standard DID was deleted successfully!')
    return redirect('/did_standardization')


@login_required
def did_standardization_edit(request, id):
    if request.method == 'GET':
        did_error = Did_Error.objects.get(id=id)
        did_error_data = {
            'id': did_error.id,
            'did': did_error.did,
            'did_status': did_error.did.isdigit(),
            'customer': did_error.customer,
            'customer_status': False if check_customer(did_error.customer) == True else True,
            'reseller': did_error.reseller,
            'in_method': did_error.in_method,
            'in_method_status': True if did_error.in_method.lower() == 'yes' or did_error.in_method.lower() == 'no' or did_error.in_method == '' else False,
            'status': did_error.status,
            'status_status': False if check_service_status(did_error.status) == True else True,
            'change_date': did_error.change_date,
            'change_date_status': not is_date(did_error.change_date),
            'voice_carrier': did_error.voice_carrier,
            'voice_carrier_status': False if check_voice_sms_carrier(did_error.voice_carrier) == True else True,
            'sms_carrier': did_error.sms_carrier,
            'sms_carrier_status': False if check_voice_sms_carrier(did_error.sms_carrier) == True else True,
            'sms_enabled': did_error.sms_enabled,
            'sms_enabled_status': True if did_error.sms_enabled.lower() == 'yes' or did_error.sms_enabled.lower() == 'no' or did_error.sms_enabled == '' else False,
            'sms_type': did_error.sms_type,
            'sms_type_status': False if check_sms_type(did_error.sms_type) == True else True,
            'sms_campaign': did_error.sms_campaign,
            'term_location': did_error.term_location,
            'term_location_status': False if check_term_location(did_error.term_location) == True else True,
            'user_first_name': did_error.user_first_name,
            'user_last_name': did_error.user_last_name,
            'extension': did_error.extension,
            'extension_status': did_error.extension.isdigit() if did_error.extension else True,
            'email': did_error.email,
            'email_status': True if did_error.email == None or did_error.email == '' else True if re.search(email_regex, did_error.email.strip()) else False,
            'onboard_date': did_error.onboard_date,
            'onboard_date_status': not is_date(did_error.onboard_date),
            'note': did_error.note,
            'e911_enabled_billed': did_error.e911_enabled_billed,
            'e911_enabled_billed_status': True if did_error.e911_enabled_billed.lower() == 'yes' or did_error.e911_enabled_billed.lower() == 'no' or did_error.e911_enabled_billed == '' else False,
            'e911_cid': did_error.e911_cid,
            'e911_cid_status': did_error.e911_cid.isdigit() if did_error.e911_cid else True,
            'e911_address': did_error.e911_address,
            'service_1': did_error.service_1,
            'service_1_status': False if check_service_item(did_error.service_1) == True else True,
            'service_2': did_error.service_2,
            'service_2_status': False if check_service_item(did_error.service_2) == True else True,
            'service_3': did_error.service_3,
            'service_3_status': False if check_service_item(did_error.service_3) == True else True,
            'service_4': did_error.service_4,
            'service_4_status': False if check_service_item(did_error.service_4) == True else True,
            'updated_date_time': did_error.updated_date_time,
            'updated_date_time_status': not is_date(did_error.updated_date_time),
            'updated_by': did_error.updated_by,
        }

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

        return render(request, 'non_standard_did_edit.html', {'did': did_error_data, 'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': voice_carrier, 'sms_type': sms_type, 'term_location': term_location, 'services': services})
    else:
        try:
            did = Did(
                did = int(request.POST['did']) if request.POST['did'].isdigit() else None,
                customer = Customer.objects.get(record_id = int(request.POST['customer'])) if request.POST['customer'] else None,
                reseller = request.POST['reseller'],
                in_method = request.POST['in_method'],
                status = Status.objects.get(record_id = int(request.POST['status'])) if request.POST['status'] else None,
                change_date = parse_date(request.POST['change_date']),
                voice_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['voice_carrier'])) if request.POST['voice_carrier'] else None,
                sms_enabled = request.POST['sms_enabled'],
                sms_carrier = Voice_Carrier.objects.get(record_id = int(request.POST['sms_carrier'])) if request.POST['sms_carrier'] else None,
                sms_type = SMS_Type.objects.get(record_id = int(request.POST['sms_type'])) if request.POST['sms_type'] else None,
                sms_campaign = request.POST['sms_campaign'],
                term_location = Term_Location.objects.get(record_id = int(request.POST['term_location'])) if request.POST['term_location'] else None,
                user_first_name = request.POST['user_first_name'],
                user_last_name = request.POST['user_last_name'],
                extension = int(request.POST['extension']) if request.POST['extension'].isdigit() else None,
                email = is_valid_email(request.POST['email']),
                onboard_date = parse_date(request.POST['onboard_date']),
                note = request.POST['note'],
                e911_enabled_billed = request.POST['e911_enabled_billed'],
                e911_cid = int(request.POST['e911_cid']) if request.POST['e911_cid'].isdigit() else None,
                e911_address = request.POST['e911_address'],
                did_uuid = uuid.uuid4(),
                service_1 = Service.objects.get(record_id = int(request.POST['service_1'])) if request.POST['service_1'] else None,
                service_2 = Service.objects.get(record_id = int(request.POST['service_2'])) if request.POST['service_2'] else None,
                service_3 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None,
                service_4 = Service.objects.get(record_id = int(request.POST['service_3'])) if request.POST['service_3'] else None,
                updated_date_time = datetime.datetime.now(),
                updated_by = request.user,
                )
            
            did.full_clean()
            did.save()

            did_error = Did_Error.objects.get(id=id)
            did_error.delete()
            
            messages.success(request, f"{request.POST['did']} was standardized successfully.")
        except Exception as e:
            messages.warning(request, e)

        return redirect('/did_standardization')


@login_required
def multi_standardization(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)

        for item in request_data:
            try:
                new_did = Did(
                    did_uuid = uuid.uuid4(), 
                    did = int(item['did']) if item['did'] else None, 
                    in_method = switch(item['in_method']), 
                    voice_carrier = Voice_Carrier.objects.get(record_id = int(item['voice_carrier'])) if item['voice_carrier'].isdigit() else None, 
                    status = Status.objects.get(record_id = int(item['status'])) if item['status'].isdigit() else None,
                    change_date =  datetime.datetime.now(), 
                    sms_enabled = switch(item['in_method']), 
                    sms_carrier = Voice_Carrier.objects.get(record_id = int(item['sms_carrier'])) if item['sms_carrier'].isdigit() else None,
                    sms_type = SMS_Type.objects.get(record_id = int(item['sms_type'])) if item['sms_type'].isdigit() else None,
                    sms_campaign = item['sms_campaign'],
                    term_location = Term_Location.objects.get(record_id = int(item['term_location'])) if item['term_location'].isdigit() else None,
                    customer = Customer.objects.get(record_id = int(item['customer'])) if item['customer'].isdigit() else None,
                    reseller = item['reseller'],
                    user_first_name = item['user_first_name'],
                    user_last_name = item['user_last_name'],
                    extension = int(item['extension']) if item['extension'].isdigit() else None,
                    email = item['email'],
                    onboard_date = parse_date(item['onboard_date']),
                    note = item['note'],
                    e911_enabled_billed = switch(item['e911_enabled_billed']),
                    e911_cid = int(item['e911_cid']) if item['e911_cid'].isdigit() else None,
                    e911_address = item['e911_address'],
                    service_1 = Service.objects.get(record_id = int(item['service_1'])) if item['service_1'].isdigit() else None,
                    service_2 = Service.objects.get(record_id = int(item['service_2'])) if item['service_2'].isdigit() else None,
                    service_3 = Service.objects.get(record_id = int(item['service_3'])) if item['service_3'].isdigit() else None,
                    service_4 = Service.objects.get(record_id = int(item['service_4'])) if item['service_4'].isdigit() else None,
                    updated_date_time = datetime.datetime.now(),
                    updated_by = item['updated_by'],
                )
                new_did.save()

                error_did = Did_Error(id = int(item['id']))
                error_did.delete()
                
            except Exception as e:
                messages.warning(request, e)

        messages.success(request, 'Multi Standardization was successflly.')
        return redirect('/did_standardization')
