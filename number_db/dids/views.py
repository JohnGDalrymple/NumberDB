from django.shortcuts import render, redirect
from .models import Did
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import unicodedata

# Create your views here.

def parse_date(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y').date() if date_string else None

def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S') if datetime_string else None

def service_type_switch(value):
    if value == "F":
        return "Fusion"
    elif value == "T":
        return "Teams"
    elif value == "HS":
        return "Hosted SMS"
    elif value == "PK":
        return "Parked"
    elif value == "IV":
        return "Inventory"
    elif value == "EF":
        return "Efax"
    elif value == "OP":
        return "Orphaned"
    elif value == "CL":
        return "Comelit"

    elif value == "fusion":
        return "F"
    elif value == "Teams":
        return "T"
    elif value == "Hosted SMS":
        return "HS"
    elif value == "Parked":
        return "PK"
    elif value == "Inventory":
        return "IV"
    elif value == "Efax":
        return "EF"
    elif value == "Orphaned":
        return "OP"
    elif value == "Comelit":
        return "CL"
    return ""
    
def voice_carrier_switch(value):
    if value == "IW":
        return "INTQ - Wholesale"
    elif value == "IO":
        return "INTQ - OC"
    elif value == "TWI":
        return "Twilio"
    
    elif value == "INTQ - Wholesale":
        return "IW"
    elif value == "INTQ - OC":
        return "IO"
    elif value == "Twilio":
        return "TWI"
    return ""
    
def sms_carrier_switch(value):
    if value == "INTQ":
        return "INTQ"
    elif value == "TWL":
        return "Twilio"
    
    elif value == "INTQ":
        return "INTQ"
    elif value == "Twilio":
        return "TWL"
    return ""
    
def status_switch(value):
    if value == "A":
        return "Active"
    elif value == "D":
        return "Disco"
    
    elif value == "Active":
        return "A"
    elif value == "Disco":
        return "D"
    return ""
    
def switch(value):
    if value == "Y":
        return "Yes"
    elif value == "N":
        return "No"
    
    elif value == "Yes":
        return "Y"
    elif value == "No":
        return "N"
    return ""

def sms_type_switch(value):
    if value == "YP":
        return "Yak Personal"
    elif value == "YS":
        return "Yak Shared"
    elif value == "YB":
        return "Yak Personal and Shared"
    elif value == "IA":
        return "INTQ API"
    elif value == "CL":
        return "Clerk"
    elif value == "SI":
        return "SIP/Simple"
    
    elif value == "Yak Personal":
        return "YP"
    elif value == "Yak Shared":
        return "YS"
    elif value == "Yak Personal and Shared":
        return "YB"
    elif value == "INTQ API":
        return "IA"
    elif value == "Clerk":
        return "CL"
    elif value == "SIP/Simple":
        return "SI"
    return ""
    
def term_location_switch(value):
    if value == "SE":
        return "SBC - East"
    elif value == "SW":
        return "SBC - West"
    elif value == "HE":
        return "Hosted - East"
    elif value == "HW":
        return "Hosted - West"
    elif value == "OC":
        return "OP - Operator Connect"
    
    elif value == "SBC - East":
        return "SE"
    elif value == "SBC - West":
        return "SW"
    elif value == "Hosted - East":
        return "HE"
    elif value == "Hosted - West":
        return "HW"
    elif value == "OP - Operator Connect":
        return "OC"
    return ""

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def list(request):
    if 'GET' == request.method:
        dids_list = Did.objects.all()
        # paginator = Paginator(dids_list, 10)
        # page = request.GET.get('page')
        # try:
        #     dids = paginator.page(page)
        # except PageNotAnInteger:
        #     dids = paginator.page(1)
        # except EmptyPage:
        #     dids = paginator.page(paginator.num_pages)

        temp = dids_list.values()

        for item in temp:
            item['in_method'] = switch(item['in_method'])
            item['voice_carrier'] = status_switch(item['voice_carrier'])
            item['status'] = status_switch(item['status'])
            item['type'] = service_type_switch(item['type'])
            item['sms_enabled'] = switch(item['sms_enabled'])
            item['sms_carrier'] = sms_carrier_switch(item['sms_carrier'])
            item['sms_type'] = sms_type_switch(item['sms_type'])
            item['term_location'] = term_location_switch(item['term_location'])
            item['e911_enabled_billed'] = switch(item['e911_enabled_billed'])
                
        return render(request, 'list.html', {'dids': temp})

    
    if 'POST' == request.method:
            try:
                csv_file = request.FILES["csv_file"]

                if len(csv_file) == 0:
                    messages.warning(request, 'Empty File')
                    return render(request, 'list.html')

                if not csv_file.name.endswith('.csv'):
                    messages.warning(request, 'File is not CSV type')
                    return render(request, 'list.html')

                if csv_file.multiple_chunks():
                    messages.warning(request, 'Uploaded file is too big (%.2f MB).' % (csv_file.size / (1000 * 1000),))
                    return render(request, 'list.html')

                file_data = csv_file.read().decode("utf-8")
                file_data = unicodedata.normalize("NFC", file_data).replace('\r', '\n')

                file_data = file_data.replace('\ufeff', '')
                lines = file_data.strip().split('\n')
                headers = lines[0].split(',')

                convert_data = []

                for line in lines[1:]:
                    fields = line.split(',')
                    if len(fields) != len(headers):
                        continue
                    convert_data.append({headers[i]: '' if fields[i] == '#N/A' else fields[i] for i in range(len(headers))})
                
                for item in convert_data:
                    save_data = Did(
                    did_uuid = item['did_uuid'], 
                    did = int(item['did']) if item['did'].isdigit() else None, 
                    in_method = switch(item['in_method']), 
                    voice_carrier = voice_carrier_switch(item['voice_carrier']), 
                    status = status_switch(item['status']), 
                    change_date = parse_date(item['change_date']), 
                    type = service_type_switch(item['type']), 
                    sms_enabled = switch(item['sms_enabled']), 
                    sms_carrier = sms_carrier_switch(item['sms_carrier']), 
                    sms_type = sms_type_switch(item['sms_type']), 
                    sms_campaign = item['sms_campaign'], 
                    term_location = term_location_switch(item['term_location']), 
                    customer = item['customer'], 
                    reseller_msp = item['reseller_msp'], 
                    user_first_name = item['user_first_name'], 
                    user_last_name = item['user_last_name'], 
                    extension = int(item['extension']) if item['extension'].isdigit() else None,
                    email = item['email'], 
                    onboard_date = parse_date(item['onboard_date']), 
                    note = item['note'], 
                    e911_enabled_billed = switch(item['e911_enabled_billed']), 
                    e911_cid = int(item['e911_cid']) if item['e911_cid'].isdigit() else None, 
                    e911_address = item['e911_address'], 
                    service_1 = item['service_1'], 
                    service_2 = item['service_2'], 
                    service_3 = item['service_3'], 
                    service_4 = item['service_4'], 
                    update_date_time = parse_datetime(item['updated_date_time']), 
                    update_by = item['updated_by'], 
                    )
                    save_data.save()

                messages.success(request, "Successfully Uploaded CSV File and Added to database")
                return redirect('/list')

            except Exception as e:
                messages.warning(request, "Unable to upload file. " + e)
                return redirect('/list')
