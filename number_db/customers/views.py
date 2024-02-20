from django.shortcuts import render, redirect
import csv
from .models import Customer
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
import math
import numpy as np
from django.db.models import Q
import os
import requests
import re

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def is_valid_email(email):
    if email == None:
        return None
    elif ',' in email:
        return email
    elif(re.search(email_regex,email)):  
        return email  
    else:  
        return email + '@outlook.com'

# Create your views here.

init_header = ['Customer full name', 'Phone', 'Fax', 'Mobile', 'Email', 'Billing address', 'Billing city', 'Billing state', 'Billing ZIP code', 'Billing country', 'E911 address', 'E911 city', 'E911 state', 'E911 ZIP code', 'E911 country']

check_header = ['AltPhone', 'AssignedTo', 'AssignedTo_RecordID', 'Balance', 'BillAddressAddr1', 'BillAddressAddr2', 'BillAddressAddr3', 'BillAddressAddr4', 'BillAddressAddr5', 'BillAddressAttentionTo', 'BillAddressCity', 'BillAddressCountry', 'BillAddressPostalCode', 'BillAddressState', 'Campaign', 'Campaign_RecordID', 'Class', 'Class_RecordID', 'CompanyName', 'CreatedDate', 'Currency', 'Currency_RecordID', 'CustomerType', 'CustomerType_RecordID', 'DeliveryMethod', 'DeliveryMethod_RecordID', 'DirectDial', 'Email', 'EntityType', 'Fax', 'FirstName', 'FullName', 'IsActive', 'IsLeadStatusOnly', 'IsStatementWithParent', 'IsTaxable', 'JobComments', 'LastActivityCompletedDate', 'LastCompletedActivity', 'LastCompletedActivity_RecordID', 'LastInvoiceRecordID', 'LastInvoiceRecordID_RecordID', 'LastInvoiceRecordIDAmount', 'LastInvoiceRecordIDTxnDate', 'LastModifiedDate', 'LastName', 'LastSalesReceiptRecordID', 'LastSalesReceiptRecordID_RecordID', 'LastSalesReceiptRecordIDTotalAmount', 'LastSalesReceiptRecordIDTxnDate', 'Latitude', 'LeadConvertedDate', 'LeadRating', 'LeadRating_RecordID', 'LeadSource', 'LeadSource_RecordID', 'LeadStatus', 'LeadStatus_RecordID', 'LifetimeValue', 'ListID', 'Longitude', 'MergeOnNextSyncTo', 'MergeOnNextSyncTo_RecordID', 'MIActiveTypeNumberCount', 'MiddleName', 'MIDiscoTypeNumberCount', 'MIDiscreteNumbers', 'MIParkedTypeNumberCount', 'Mobile', 'Name', 'NextActivityDueDate', 'NextPendingActivity', 'NextPendingActivity_RecordID', 'Notes', 'Pager', 'ParentFullName', 'ParentFullName_RecordID', 'Phone', 'PortalPassword', 'PortalUserName', 'PrintAs', 'RecordID', 'ResaleNumber', 'SalesRepName', 'SalesRepRecordID', 'SalesTaxCode', 'SalesTaxCode_RecordID', 'SalesTaxCountry', 'Salutation', 'ShipAddressAddr1', 'ShipAddressAddr2', 'ShipAddressAddr3', 'ShipAddressAddr4', 'ShipAddressAddr5', 'ShipAddressAttentionTo', 'ShipAddressCity', 'ShipAddressCountry', 'ShipAddressPostalCode', 'ShipAddressState', 'Sublevel', 'Suffix', 'TaxExemptionReason', 'TaxExemptionReason_RecordID', 'Terms', 'Terms_RecordID', 'TimeModifiedAccounting', 'TotalBalance']

default_data_header = ['full_name', 'phone', 'fax', 'mobile', 'email', 'billing_address', 'billing_city', 'billing_state', 'billing_zipcode', 'billing_country', 'e911_address', 'e911_city', 'e911_state', 'e911_zipcode', 'e911_country']

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
            data = Customer.objects.filter(id = int(id)).values()
            writer.writerow([
                data[0]['full_name'],
                data[0]['phone'],
                data[0]['fax'],
                data[0]['mobile'],
                data[0]['email'],
                data[0]['billing_address'],
                data[0]['billing_city'],
                data[0]['billing_state'],
                data[0]['billing_zipcode'],
                data[0]['billing_country'],
                data[0]['e911_address'],
                data[0]['e911_city'],
                data[0]['e911_state'],
                data[0]['e911_zipcode'],
                data[0]['e911_country'],
                ])

        return response

    else:
        messages.warning(request, 'Please slect in this table')
        return redirect('/customer')


@login_required
def customer_list(request):
    if 'GET' == request.method:
        customers_list = []
        if request.GET:
            query = request.GET['search']
            q_objects = Q()
            for field in default_data_header:
                q_objects |= Q(**{field + '__icontains': query})

            customers_list = Customer.objects.filter(q_objects).distinct().values()

            for item in customers_list:
                item['full_name'] =  "" if(item['full_name'] == None) else item['full_name']
                item['phone'] =  "" if(item['phone'] == None) else item['phone']
                item['fax'] =  "" if(item['fax'] == None) else item['fax']
                item['mobile'] =  "" if(item['mobile'] == None) else item['mobile']
                item['email'] =  "" if(item['email'] == None) else item['email']
                item['billing_address'] =  "" if(item['billing_address'] == None) else item['billing_address']
                item['billing_city'] =  "" if(item['billing_city'] == None) else item['billing_city']
                item['billing_state'] =  "" if(item['billing_state'] == None) else item['billing_state']
                item['billing_zipcode'] =  "" if(item['billing_zipcode'] == None) else item['billing_zipcode']
                item['billing_country'] =  "" if(item['billing_country'] == None) else item['billing_country']
                item['e911_address'] =  "" if(item['e911_address'] == None) else item['e911_address']
                item['e911_city'] =  "" if(item['e911_city'] == None) else item['e911_city']
                item['e911_state'] =  "" if(item['e911_state'] == None) else item['e911_state']
                item['e911_zipcode'] =  "" if(item['e911_zipcode'] == None) else item['e911_zipcode']
                item['e911_country'] =  "" if(item['e911_country'] == None) else item['e911_country']

            return render(request, 'customers.html', {'customers': customers_list, 'search': query})
        else:
            customers_list = Customer.objects.all().values()

            for item in customers_list:
                item['full_name'] =  "" if(item['full_name'] == None) else item['full_name']
                item['phone'] =  "" if(item['phone'] == None) else item['phone']
                item['fax'] =  "" if(item['fax'] == None) else item['fax']
                item['mobile'] =  "" if(item['mobile'] == None) else item['mobile']
                item['email'] =  "" if(item['email'] == None) else item['email']
                item['billing_address'] =  "" if(item['billing_address'] == None) else item['billing_address']
                item['billing_city'] =  "" if(item['billing_city'] == None) else item['billing_city']
                item['billing_state'] =  "" if(item['billing_state'] == None) else item['billing_state']
                item['billing_zipcode'] =  "" if(item['billing_zipcode'] == None) else item['billing_zipcode']
                item['billing_country'] =  "" if(item['billing_country'] == None) else item['billing_country']
                item['e911_address'] =  "" if(item['e911_address'] == None) else item['e911_address']
                item['e911_city'] =  "" if(item['e911_city'] == None) else item['e911_city']
                item['e911_state'] =  "" if(item['e911_state'] == None) else item['e911_state']
                item['e911_zipcode'] =  "" if(item['e911_zipcode'] == None) else item['e911_zipcode']
                item['e911_country'] =  "" if(item['e911_country'] == None) else item['e911_country']

            return render(request, 'customers.html', {'customers': customers_list})
    
    if 'POST' == request.method:
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
                
                if data_dict != []:
                    if set(data_dict[0].keys()) == set(check_header):
                        filter_data = data_df.fillna('')
                        filter_data = filter_data.to_dict('records')
                        for item in filter_data:
                            save_data = Customer(
                            full_name = item['FullName'],
                            phone = item['Phone'],
                            fax = item['Fax'],
                            mobile = item['Mobile'],
                            email = item['Email'],
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
                            record_id = item['RecordID'],
                            is_active = item['IsActive'],
                            )
                            try:
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
    customer = Customer.objects.get(id=id)
    customer.full_name = customer.full_name + " (deleted)"
    customer.is_active = False
    try:
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
            phone = request.POST['phone'],
            fax = request.POST['fax'],
            mobile = request.POST['mobile'],
            email = request.POST['email'],
            billing_address = request.POST['billing_address'],
            billing_city = request.POST['billing_city'],
            billing_state = request.POST['billing_state'],
            billing_country = request.POST['billing_country'],
            e911_address = request.POST['e911_address'],
            e911_city = request.POST['e911_city'],
            e911_state = request.POST['e911_state'],
            e911_zipcode = request.POST['e911_zipcode'],
            e911_country = request.POST['billing_address'],
            is_active = True,
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(), )
        try:
            customer.full_clean()
        except ValidationError as e:
            messages.warning(request, e)

        customer.save()
        messages.success(request, 'Customer was created successfully!')
        return redirect('/customer')
    else:
        return render(request, 'customer_create.html')
    
@login_required
def customer_edit(request, id):
    customer = Customer.objects.filter(id=id).values()[0]
    context = {'customer': customer}
    return render(request, 'customer_edit.html', context)

@login_required
def customer_update(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == "POST":
        customer.full_name = request.POST['full_name']
        customer.phone = request.POST['phone']
        customer.fax = request.POST['fax']
        customer.mobile = request.POST['mobile']
        customer.email = request.POST['email']
        customer.billing_address = request.POST['billing_address']
        customer.billing_city = request.POST['billing_city']
        customer.billing_state = request.POST['billing_state']
        customer.billing_zipcode = request.POST['billing_zipcode']
        customer.billing_country = request.POST['billing_country']
        customer.e911_address = request.POST['e911_address']
        customer.e911_city = request.POST['e911_city']
        customer.e911_state = request.POST['e911_state']
        customer.e911_zipcode = request.POST['e911_zipcode']
        customer.e911_country = request.POST['e911_country']
        customer.updated_at = datetime.datetime.now()
        try:
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
        params = {'skip': skip, 'top': top, 'select':'RecordID,FullName,Phone,Fax,Mobile,Email,BillAddressAddr1,BillAddressCity,BillAddressState,BillAddressPostalCode,BillAddressCountry,ShipAddressAddr1,ShipAddressCity,ShipAddressCountry,ShipAddressPostalCode,ShipAddressState,IsActive'}

        response = requests.get(f"{os.getenv('METHOD_GET_TABLE_ENDPOINT')}Customer", headers=headers, params=params)

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
            record_id = item['RecordID'],
            is_active = item['IsActive'],
            )
            try:
                save_data.save()
            except Exception as e:
                messages.warning(request, e)

        skip += 100
    
    messages.success(request, "Customer data has been synchronized with Method.")
        
    return redirect('/customer')
