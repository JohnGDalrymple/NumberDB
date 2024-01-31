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
# Create your views here.

default_header = ['Customer full name', 'Phone', 'Fax', 'Mobile', 'Email', 'Billing address', 'Billing city', 'Billing state', 'Billing ZIP code', 'Billing country', 'E911 address', 'E911 city', 'E911 state', 'E911 ZIP code', 'E911 country']

@login_required
def index(request):
    return render(request, 'index.html')

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
            item['e911address'] =  "" if(item['e911address'] == None) else item['e911address']
            item['e911city'] =  "" if(item['e911city'] == None) else item['e911city']
            item['e911state'] =  "" if(item['e911state'] == None) else item['e911state']
            item['e911zipcode'] =  "" if(item['e911zipcode'] == None) else item['e911zipcode']
            item['e911country'] =  "" if(item['e911country'] == None) else item['e911country']

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
                
                file_data = csv_file.read().decode("utf-8")
                file_data = unicodedata.normalize("NFC", file_data).replace('\r', '\n')

                file_data = file_data.replace('\ufeff', '')
                lines = file_data.strip().split('\n')
                headers = lines[0].split(',')

                
            else:
                messages.warning(request, "Please upload CSV file.")
        
        except Exception as e:
            messages.warning(request, "Unable to upload file." + e)
        
        return redirect('/customer')


    
@login_required
def customer_delete(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    messages.warning(request, 'Customer was deleted successfully!')
    return redirect('/customer')