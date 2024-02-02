from django.shortcuts import render, redirect
import csv
from .models import Did
from django.db.models import Q
from customers.models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dids.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
import unicodedata
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
import uuid
# Create your views here.

default_data_header = ['did', 'customer', 'reseller', 'in_method', 'status', 'change_date', 'voice_carrier', 'type', 'sms_enabled', 'sms_carrier', 'sms_type', 'sms_campaign', 'term_location', 'user_first_name', 'user_last_name', 'extension', 'email', 'onboard_date', 'note', 'e911_enabled_billed', 'e911_cid', 'e911_address', 'did_uuid', 'service_1', 'service_2', 'service_3', 'service_4', 'updated_date_time', 'updated_by']

default_header = ['DID', 'Customer', 'Reseller', 'In Method', 'Status', 'Change Date', 'Voice Carrier', 'Type', 'SMS Enabled', 'SMS Carrier', 'SMS Type', 'SMS Campaign', 'Term Location', 'User First Name', 'User Last Name', 'Extension', 'Email', 'Onboard Date', 'Note', 'E911 Enabled Billed', 'E911 CID', 'E911 Address', 'DID uuid', 'Service 1', 'Service 2', 'Service 3', 'Service 4', 'Updated Date Time', 'Updated By']

def parse_date(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y').date() if date_string else None

def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, '%m/%d/%Y %H:%M:%S') if datetime_string else None

def service_type_switch(value):
    if value.lower() == "fusion":
        return "Fusion"
    elif value.lower() == "teams":
        return "Teams"
    elif value.lower() == "hosted sms":
        return "Hosted SMS"
    elif value.lower() == "parked":
        return "Parked"
    elif value.lower() == "inventory":
        return "Inventory"
    elif value.lower() == "efax":
        return "Efax"
    elif value.lower() == "orphaned":
        return "Orphaned"
    elif value.lower() == "comelit":
        return "Comelit"
    return ""
    
def voice_carrier_switch(value):
    if value.lower() == "intq - wholesale":
        return "INTQ - Wholesale"
    elif value.lower() == "intq - oc":
        return "INTQ - OC"
    elif value.lower() == "twilio":
        return "Twilio"
    return ""
    
def sms_carrier_switch(value):
    if value.lower() == "intq":
        return "INTQ"
    elif value.lower() == "twilio":
        return "TWL"
    return ""
    
def status_switch(value):
    if value.lower() == "active":
        return "Active"
    elif value.lower() == "disco":
        return "Disco"
    return ""
    
def switch(value):
    if value.lower() == "yes":
        return "Yes"
    elif value.lower() == "no":
        return "No"
    return ""

def sms_type_switch(value):
    if value.lower() == "yak personal":
        return "Yak Personal"
    elif value.lower() == "yak shared":
        return "Yak Shared"
    elif value.lower() == "yak personal and shared":
        return "Yak Personal and Shared"
    elif value.lower() == "intq api":
        return "INTQ API"
    elif value.lower() == "clerk":
        return "Clerk"
    elif value.lower() == "sip/simple":
        return "SIP/Simple"
    return ""
    
def term_location_switch(value):
    if value.lower() == "sbc - east":
        return "SBC - East"
    elif value.lower() == "sbc - west":
        return "SBC - West"
    elif value.lower() == "hosted - east":
        return "Hosted - East"
    elif value.lower() == "hosted - west":
        return "Hosted - West"
    elif value.lower() == "op - operator connect":
        return "OP - Operator Connect"
    return ""

@login_required
def index(request):
    return render(request, 'index.html')

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
            data = Did.objects.filter(id = int(id)).values()
            writer.writerow([
                data[0]['did'],
                data[0]['customer'],
                data[0]['reseller'],
                data[0]['in_method'],
                data[0]['status'],
                data[0]['change_date'],
                data[0]['voice_carrier'],
                data[0]['sms_enabled'],
                data[0]['type'],
                data[0]['sms_carrier'],
                data[0]['sms_type'],
                data[0]['sms_campaign'],
                data[0]['term_location'],
                data[0]['user_first_name'],
                data[0]['user_last_name'],
                data[0]['extension'],
                data[0]['email'],
                data[0]['onboard_date'],
                data[0]['note'],
                data[0]['e911_enabled_billed'],
                data[0]['e911_cid'],
                data[0]['e911_address'],
                data[0]['did_uuid'],
                data[0]['service_1'],
                data[0]['service_2'],
                data[0]['service_3'],
                data[0]['service_4'],
                data[0]['updated_date_time'],
                data[0]['updated_by'],
                ])

        return response

    else:
        messages.warning(request, 'Please slect in this table')
        return redirect('/did')

@login_required
def did(request):
    if 'GET' == request.method:
        dids_list = []
        if request.GET:
            query = request.GET['search']
            q_objects = Q()
            for field in default_data_header:
                q_objects |= Q(**{field + '__icontains': query})

            dids_list = Did.objects.filter(q_objects).distinct().values()

            for item in dids_list:
                item['change_date'] =  "" if(item['change_date'] == None) else item['change_date']
                item['extension'] =  "" if(item['extension'] == None) else item['extension']
                item['onboard_date'] =  "" if(item['onboard_date'] == None) else item['onboard_date']
                item['e911_cid'] =  "" if(item['e911_cid'] == None) else item['e911_cid']
                item['updated_date_time'] =  "" if(item['updated_date_time'] == None) else item['updated_date_time']
                
            return render(request, 'dids.html', {'dids': dids_list, 'search': query})

        else:
            dids_list = Did.objects.all().values()

            for item in dids_list:
                item['change_date'] =  "" if(item['change_date'] == None) else item['change_date']
                item['extension'] =  "" if(item['extension'] == None) else item['extension']
                item['onboard_date'] =  "" if(item['onboard_date'] == None) else item['onboard_date']
                item['e911_cid'] =  "" if(item['e911_cid'] == None) else item['e911_cid']
                item['updated_date_time'] =  "" if(item['updated_date_time'] == None) else item['updated_date_time']
                    
            return render(request, 'dids.html', {'dids': dids_list})
    
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
                            convert_data = data_df.fillna('')
                            convert_data = convert_data.to_dict('records')

                            for item in convert_data:
                                save_data = Did(
                                did_uuid = item['DID uuid'], 
                                did = item['DID'] if item['DID'] else None, 
                                in_method = switch(item['In Method']), 
                                voice_carrier = voice_carrier_switch(item['Voice Carrier']), 
                                status = status_switch(item['Status']), 
                                change_date = parse_date(item['Change Date']), 
                                type = service_type_switch(item['Type']), 
                                sms_enabled = switch(item['SMS Enabled']), 
                                sms_carrier = sms_carrier_switch(item['SMS Carrier']), 
                                sms_type = sms_type_switch(item['SMS Type']), 
                                sms_campaign = item['SMS Campaign'], 
                                term_location = term_location_switch(item['Term Location']), 
                                customer = item['Customer'], 
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
                                service_1 = item['Service 1'], 
                                service_2 = item['Service 2'], 
                                service_3 = item['Service 3'], 
                                service_4 = item['Service 4'], 
                                updated_date_time = parse_datetime(item['Updated Date Time']), 
                                updated_by = item['Updated By'], 
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
    return render(request, 'user_create.html')

@login_required
def user_create(request):
    if request.method == "POST":
        print(request.POST)
        # form = RegistrationForm(request.POST)
        # users = User(
        #     username=form.cleaned_data['username'],
        #     password=make_password(form.cleaned_data['password1']),
        #     is_staff=True,
        #     is_active=True,
        #     is_superuser=True,
        #     email=form.cleaned_data['email'],
        #     first_name=form.cleaned_data['first_name'],
        #     last_name=form.cleaned_data['last_name'],
        # )
        # try:
        #     users.full_clean()
        # except ValidationError as e:
        #     pass
        # users.save()
        messages.success(request, 'User was created successfully!')
        return HttpResponseRedirect('/user')

@login_required
def user_update(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.date_joined = request.POST['date_joined']
        user.save()
        messages.success(request, 'User was updated successfully!')
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
        did = Did(
            did = int(request.POST['did']) if request.POST['did'].isdigit() else None,
            customer = request.POST['customer'],
            reseller = request.POST['reseller'],
            in_method = request.POST['in_method'],
            status = request.POST['status'],
            change_date = parse_date(request.POST['change_date']),
            voice_carrier = request.POST['voice_carrier'],
            type = request.POST['type'],
            sms_enabled = request.POST['sms_enabled'],
            sms_carrier = request.POST['sms_carrier'],
            sms_type = request.POST['sms_type'],
            sms_campaign = request.POST['sms_campaign'],
            term_location = request.POST['term_location'],
            user_first_name = request.POST['user_first_name'],
            user_last_name = request.POST['user_last_name'],
            extension = int(request.POST['extension']) if request.POST['extension'].isdigit() else None,
            email = request.POST['email'],
            onboard_date = parse_date(request.POST['onboard_date']),
            note = request.POST['note'],
            e911_enabled_billed = request.POST['e911_enabled_billed'],
            e911_cid = int(request.POST['e911_cid']) if request.POST['e911_cid'].isdigit() else None,
            e911_address = request.POST['e911_address'],
            did_uuid = uuid.uuid4(),
            service_1 = request.POST['service_1'],
            service_2 = request.POST['service_2'],
            service_3 = request.POST['service_3'],
            service_4 = request.POST['service_4'],
            updated_date_time = datetime.datetime.now(),
            updated_by = request.user,
            )
        try:
            did.full_clean()
        except ValidationError as e:
            messages.warning(request, e)
        did.save()
        messages.success(request, 'DID was created successfully!')
        return redirect('/did')
    else:
        customersData = Customer.objects.values_list('id', 'full_name')
        customers = []
        for item in customersData:
            customers.append({'id': item[0], 'full_name': item[1]})
        return render(request, 'did_create.html', {'customers': customers})
    
@login_required
def did_delete(request, id):
    did = Did.objects.get(id=id)
    did.delete()
    messages.warning(request, 'DID was deleted successfully!')
    return redirect('/did')

@login_required
def did_edit(request, id):
    did = Did.objects.filter(id=id).values()[0]
    didData = {
        'id': did['id'],
        'customer': did['customer'],
        'reseller': did['reseller'],
        'in_method': did['in_method'],
        'status': did['status'],
        'change_date': did['change_date'] if not did['change_date'] else did['change_date'].strftime('%Y-%m-%d'),
        'voice_carrier': did['voice_carrier'],
        'type': did['type'],
        'sms_enabled': did['sms_enabled'],
        'sms_carrier': did['sms_carrier'],
        'sms_type': did['sms_type'],
        'sms_campaign': did['sms_campaign'],
        'term_location': did['term_location'],
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
        'service_1': did['service_1'],
        'service_2': did['service_2'],
        'service_3': did['service_3'],
        'service_4': did['service_4'],
        'updated_date_time': did['updated_date_time'] if not did['updated_date_time'] else did['updated_date_time'].strftime('%Y-%m-%d'),
        'updated_by': did['updated_by'],
    }
    context = {'did': didData}
    return render(request, 'did_edit.html', context)