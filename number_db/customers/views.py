from django.shortcuts import render, redirect
import csv
from .models import Customer
from assist_dids.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import re
from io import StringIO
import pandas as pd
import numpy as np
from django.db.models import Q
import os
import requests
import re

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

# Create your views here.

init_header = ['Full name', 'Company name', 'Phone', 'Fax', 'Mobile', 'Email', 'Billing address', 'Billing city', 'Billing state', 'Billing ZIP code', 'Billing country', 'E911 address', 'E911 city', 'E911 state', 'E911 ZIP code', 'E911 country', 'Customer type', 'Support contact', 'Attachments', 'Open balance', 'Note']

default_data_header = ['full_name', 'company_name', 'phone', 'fax', 'mobile', 'email', 'billing_address', 'billing_city', 'billing_state', 'billing_zipcode', 'billing_country', 'e911_address', 'e911_city', 'e911_state', 'e911_zipcode', 'e911_country', 'support_contact', 'attachments', 'open_balance', 'note']

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def export_csv(request):
    ids = request.GET.get('pk')
    
    if (ids):
        id_array = ids.split(",")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CurrentCustomers.csv"'
        writer = csv.writer(response)
        writer.writerow(init_header)

        for id in id_array:
            data = Customer.objects.get(id = int(id))
            writer.writerow([
                data.full_name,
                data.phone,
                data.fax,
                data.mobile,
                data.email,
                data.billing_address,
                data.billing_city,
                data.billing_state,
                data.billing_zipcode,
                data.billing_country,
                data.e911_address,
                data.e911_city,
                data.e911_state,
                data.e911_zipcode,
                data.e911_country,
                data.customer_type if data.customer_type == None else data.customer_type.name,
                data.support_contact,
                data.attachments,
                data.open_balance,
                data.note,
                ])

        return response

    else:
        messages.warning(request, 'Please slect in this table')
        return redirect('/customer')


@login_required
def customer_list(request):
    if request.method == 'GET':
        customers_list = []
        if request.GET.get('search'):
            query = request.GET['search']
            q_objects = Q()
            for field in default_data_header:
                q_objects |= Q(**{field + '__icontains': query})

            q_objects |= Q(**{'customer_type__name__icontains': query})

            customers_list = Customer.objects.filter(q_objects)

            for item in customers_list:
                item.full_name =  "" if(item.full_name == None) else item.full_name
                item.company_name =  "" if(item.company_name == None) else item.company_name
                item.phone =  "" if(item.phone == None) else item.phone
                item.fax =  "" if(item.fax == None) else item.fax
                item.mobile =  "" if(item.mobile == None) else item.mobile
                item.email =  "" if(item.email == None) else item.email
                item.billing_address =  "" if(item.billing_address == None) else item.billing_address
                item.billing_city =  "" if(item.billing_city == None) else item.billing_city
                item.billing_state =  "" if(item.billing_state == None) else item.billing_state
                item.billing_zipcode =  "" if(item.billing_zipcode == None) else item.billing_zipcode
                item.billing_country =  "" if(item.billing_country == None) else item.billing_country
                item.e911_address =  "" if(item.e911_address == None) else item.e911_address
                item.e911_city =  "" if(item.e911_city == None) else item.e911_city
                item.e911_state =  "" if(item.e911_state == None) else item.e911_state
                item.e911_zipcode =  "" if(item.e911_zipcode == None) else item.e911_zipcode
                item.e911_country =  "" if(item.e911_country == None) else item.e911_country
                item.support_contact =  "" if(item.support_contact == None) else item.support_contact
                item.attachments =  "" if(item.attachments == None) else item.attachments
                item.open_balance =  "" if(item.open_balance == None) else item.open_balance
                item.note =  "" if(item.note == None) else item.note

            size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(customers_list, size)
            customers = paginator.get_page(page_number)

            return render(request, 'customers.html', {'customers': customers, 'search': query})
        else:
            customers_list = Customer.objects.all().select_related('customer_type')

            for item in customers_list:
                item.full_name =  "" if(item.full_name == None) else item.full_name
                item.company_name =  "" if(item.company_name == None) else item.company_name
                item.phone =  "" if(item.phone == None) else item.phone
                item.fax =  "" if(item.fax == None) else item.fax
                item.mobile =  "" if(item.mobile == None) else item.mobile
                item.email =  "" if(item.email == None) else item.email
                item.billing_address =  "" if(item.billing_address == None) else item.billing_address
                item.billing_city =  "" if(item.billing_city == None) else item.billing_city
                item.billing_state =  "" if(item.billing_state == None) else item.billing_state
                item.billing_zipcode =  "" if(item.billing_zipcode == None) else item.billing_zipcode
                item.billing_country =  "" if(item.billing_country == None) else item.billing_country
                item.e911_address =  "" if(item.e911_address == None) else item.e911_address
                item.e911_city =  "" if(item.e911_city == None) else item.e911_city
                item.e911_state =  "" if(item.e911_state == None) else item.e911_state
                item.e911_zipcode =  "" if(item.e911_zipcode == None) else item.e911_zipcode
                item.e911_country =  "" if(item.e911_country == None) else item.e911_country
                item.support_contact =  "" if(item.support_contact == None) else item.support_contact
                item.attachments =  "" if(item.attachments == None) else item.attachments
                item.open_balance =  "" if(item.open_balance == None) else item.open_balance
                item.note =  "" if(item.note == None) else item.note

            size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(customers_list, size)
            customers = paginator.get_page(page_number)

            return render(request, 'customers.html', {'customers': customers})
    
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
                
                data_df = pd.read_csv(csv_file)
                data_dict = data_df.to_dict('records')
                print(data_dict[0].keys())
                print(init_header)
                
                if data_dict != []:
                    if set(data_dict[0].keys()) == set(init_header):
                        filter_data = data_df.fillna('')
                        filter_data = filter_data.to_dict('records')
                        for item in filter_data:
                            try:
                                save_data = Customer(
                                full_name = item['Full name'],
                                company_name = item['Company name'],
                                phone = item['Phone'],
                                fax = item['Fax'],
                                mobile = item['Mobile'],
                                email = is_valid_email(item['Email']),
                                billing_address = item['Billing address'],
                                billing_city = item['Billing city'],
                                billing_state = item['Billing state'],
                                billing_zipcode = item['Billing ZIP code'],
                                billing_country = item['Billing country'],
                                e911_address = item['E911 address'],
                                e911_city = item['E911 city'],
                                e911_state = item['E911 state'],
                                e911_zipcode = item['E911 ZIP code'],
                                e911_country = item['E911 country'],
                                customer_type = Customer_Type.objects.get(name = item['Customer type']) if item['Customer type'] else None,
                                support_contact = item['Support contact'],
                                attachments = item['Attachments'],
                                open_balance = float(item['Open balance']) if item['Open balance'] else None,
                                note = item['Note'],
                                is_synced = False,
                                )
                                save_data.save()
                            except Exception as e:
                                messages.warning(request, e)
                        messages.success(request, "Successfully Uploaded CSV File and Added to database")
                    else:
                        messages.warning(request, "This file format is not correct. Please download `Sample CSV` and wirte the doc as it")
                else: 
                    messages.warning(request, "This file is empty!")
            else:
                messages.warning(request, "Please upload CSV file.")
        except Exception as e:
            messages.warning(request, "Unable to upload file." + e)
            return redirect('/customer')
        
        return redirect('/customer')

@login_required
def customer_delete(request, id):
    try:
        customer = Customer.objects.get(id=id)
        customer.is_active = False
        customer.is_synced = False
        
        customer.save()
        messages.warning(request, 'Customer was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/customer')

@login_required
def customer_add(request):
    if request.method == 'POST':
        customer = Customer(
            full_name = request.POST['full_name'],
            company_name = request.POST['company_name'],
            phone = request.POST['phone'],
            fax = request.POST['fax'],
            mobile = request.POST['mobile'],
            email = is_valid_email(request.POST['email']),
            billing_address = request.POST['billing_address'],
            billing_city = request.POST['billing_city'],
            billing_state = request.POST['billing_state'],
            billing_country = request.POST['billing_country'],
            e911_address = request.POST['e911_address'],
            e911_city = request.POST['e911_city'],
            e911_state = request.POST['e911_state'],
            e911_zipcode = request.POST['e911_zipcode'],
            e911_country = request.POST['billing_address'],
            customer_type_id = request.POST['customer_type'],
            support_contact = request.POST['support_contact'],
            attachments = request.POST['attachments'],
            open_balance = float(request.POST['open_balance']) if request.POST['open_balance'] else 0,
            note = request.POST['note'],
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
            )
        try:
            customer.full_clean()
        except ValidationError as e:
            messages.warning(request, e)

        customer.save()
        messages.success(request, 'Customer was created successfully!')
        return redirect('/customer')
    else:
        customer_types = Customer_Type.objects.all()
        return render(request, 'customer_create.html', {'customer_types': customer_types})
    
@login_required
def customer_edit(request, id):
    customer_types = Customer_Type.objects.all()
    customer = Customer.objects.get(id=id)
    context = {'customer': customer, 'customer_types': customer_types}
    return render(request, 'customer_edit.html', context)

@login_required
def customer_update(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == "POST":
        try:
            customer.full_name = request.POST['full_name']
            customer.company_name = request.POST['company_name']
            customer.phone = request.POST['phone']
            customer.fax = request.POST['fax']
            customer.mobile = request.POST['mobile']
            customer.email = is_valid_email(request.POST['email'])
            customer.billing_address = request.POST['billing_address']
            customer.billing_city = request.POST['billing_city']
            customer.billing_state = request.POST['billing_state']
            customer.billing_country = request.POST['billing_country']
            customer.e911_address = request.POST['e911_address']
            customer.e911_city = request.POST['e911_city']
            customer.e911_state = request.POST['e911_state']
            customer.e911_zipcode = request.POST['e911_zipcode']
            customer.e911_country = request.POST['billing_address']
            customer.customer_type = Customer_Type.objects.get(record_id = request.POST['customer_type'])
            customer.support_contact = request.POST['support_contact']
            customer.attachments = request.POST['attachments']
            customer.open_balance = float(request.POST['open_balance']) if request.POST['open_balance'] else 0
            customer.note = request.POST['note']
            customer.is_synced = False
            customer.updated_at = datetime.datetime.now()
            customer.save()
            messages.success(request, 'Customer was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/customer')

@login_required
def sync_method(request):
    skip = 0
    top = 100
    headers = {'Authorization': 'APIKey ' +  os.getenv('METHOD_API_KEY')}
    while True:
        params = {'skip': skip, 'top': top, 'select':'RecordID,FullName,Phone,Fax,Mobile,Email,BillAddressAddr1,BillAddressCity,BillAddressState,BillAddressPostalCode,BillAddressCountry,ShipAddressAddr1,ShipAddressCity,ShipAddressCountry,ShipAddressPostalCode,ShipAddressState,CustomerType_RecordID,CompanyName,Notes,Balance', 'filter': "IsActive eq true and Sublevel eq 0 and not (CompanyName eq '')"}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}Entity", headers=headers, params=params)

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
            save_data = Customer(
            full_name = item['FullName'],
            company_name = item['CompanyName'],
            phone = item['Phone'],
            fax = item['Fax'],
            mobile = item['Mobile'],
            email = is_valid_email(item['Email']),
            billing_address = item['BillAddressAddr1'],
            billing_city = item['BillAddressCity'],
            billing_state = item['BillAddressState'],
            billing_zipcode = item['BillAddressPostalCode'],
            billing_country = item['BillAddressCountry'],
            e911_address = item['ShipAddressAddr1'],
            e911_city = item['ShipAddressCity'],
            e911_state = item['ShipAddressState'],
            e911_zipcode = item['ShipAddressPostalCode'],
            e911_country = item['ShipAddressCountry'],
            customer_type = Customer_Type.objects.get(record_id = int(item['CustomerType_RecordID'])) if item['CustomerType_RecordID'] else None,
            open_balance = float(item['Balance']),
            note = item['Notes'],
            record_id = item['RecordID'],
            is_synced = True,
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)
        print("here is the one length", len(response_json['value']))
        skip += 100
    
    messages.success(request, "Customer data has been synchronized with Method.")
        
    return redirect('/customer')
