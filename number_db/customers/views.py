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
import unicodedata
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import re
from io import StringIO
import pandas as pd
import math
import numpy as np

# Create your views here.

default_header = ['Customer full name', 'Phone', 'Fax', 'Mobile', 'Email', 'Billing address', 'Billing city', 'Billing state', 'Billing ZIP code', 'Billing country', 'E911 address', 'E911 city', 'E911 state', 'E911 ZIP code', 'E911 country']

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
        writer.writerow(default_header)

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
                    if list(data_dict[0].keys()) == default_header:
                        filter_data = data_df.fillna('')
                        filter_data = filter_data.to_dict('records')
                        for item in filter_data:
                            save_data = Customer(
                            full_name = item['Customer full name'],
                            phone = item['Phone'],
                            fax = item['Fax'],
                            mobile = item['Mobile'],
                            email = item['Email'],
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
    customer.delete()
    messages.warning(request, 'Customer was deleted successfully!')
    return redirect('/customer')

@login_required
def customer_add(request):
    if request.method == 'POST':
        customer = Customer(
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            fax=request.POST['fax'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
            billing_address=request.POST['billing_address'],
            billing_city=request.POST['billing_city'],
            billing_state=request.POST['billing_state'],
            billing_country=request.POST['billing_country'],
            e911_address=request.POST['e911_address'],
            e911_city=request.POST['e911_city'],
            e911_state=request.POST['e911_state'],
            e911_zipcode=request.POST['e911_zipcode'],
            e911_country=request.POST['billing_address'],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(), )
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