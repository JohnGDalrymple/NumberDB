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

# Create your views here.

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


def check_voice_carrier(voice_carrier_value):
    try:
        voice_carrier = Voice_Carrier.objects.get(name__iexact = voice_carrier_value)
        return voice_carrier
    except Exception as e:
        return True if voice_carrier_value else None
    

def check_sms_carrier(sms_carrier_value):
    try:
        sms_carrier = SMS_Carrier.objects.get(name__iexact = sms_carrier_value)
        return sms_carrier
    except Exception as e:
        return True if sms_carrier_value else None
    

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


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def did(request):
    if 'GET' == request.method:
        did_error = Did_Error.objects.all().values()
        dids_list = []
        if request.GET:
            query = request.GET['search']

            # dids_list = Did.objects.filter(q_objects).distinct().values()
            q_objects = []
            q_objects.append((Q(did__icontains = query)))
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
            q_objects.append((Q(service_1__icontains = query)))
            q_objects.append((Q(service_2__icontains = query)))
            q_objects.append((Q(service_3__icontains = query)))
            q_objects.append((Q(service_4__icontains = query)))
            q_objects.append((Q(updated_by__icontains = query)))
            
            # Add Q objects for foreign key fields
            q_objects.append((Q(status__name__icontains = query)))
            q_objects.append((Q(voice_carrier__name__icontains = query)))
            q_objects.append((Q(sms_carrier__name__icontains = query)))
            q_objects.append((Q(sms_type__name__icontains = query)))
            q_objects.append((Q(term_location__name__icontains = query)))
            q_objects.append((Q(customer__full_name__icontains = query)))
            q_objects.append((Q(reseller__full_name__icontains = query)))
            
            # Use Q object to query the database with OR condition
            dids_list = Did.objects.filter(reduce(or_, q_objects))

            for item in dids_list:
                item.change_date =  "" if(item.change_date == None) else item.change_date
                item.extension =  "" if(item.extension == None) else item.extension
                item.onboard_date =  "" if(item.onboard_date == None) else item.onboard_date
                item.e911_cid =  "" if(item.e911_cid == None) else item.e911_cid
                item.updated_date_time =  "" if(item.updated_date_time == None) else item.updated_date_time
                
            return render(request, 'dids.html', {'dids': dids_list, 'search': query, 'error': did_error})

        else:
            # dids_list = Did.objects.all().values()
            dids_list = Did.objects.all().select_related('customer', 'reseller', 'status', 'voice_carrier', 'sms_carrier', 'sms_type', 'term_location')
            for item in dids_list:
                item.change_date =  "" if(item.change_date == None) else item.change_date
                item.extension =  "" if(item.extension == None) else item.extension
                item.onboard_date =  "" if(item.onboard_date == None) else item.onboard_date
                item.e911_cid =  "" if(item.e911_cid == None) else item.e911_cid
                item.updated_date_time =  "" if(item.updated_date_time == None) else item.updated_date_time
                    
            return render(request, 'dids.html', {'dids': dids_list, 'error': did_error})
    
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
                        if set(data_dict[0].keys()) == set(default_header):
                            convert_data = data_df.fillna('')
                            convert_data = convert_data.to_dict('records')

                            error_flag = False

                            for item in convert_data:
                                customer_value = check_customer(item['Customer'])
                                resller_value = check_customer(item['Reseller'])
                                service_status_value = check_service_status(item['Status'])
                                voice_carrier_value = check_voice_carrier(item['Voice Carrier'])
                                sms_carrier_value = check_sms_carrier(item['SMS Carrier'])
                                sms_type_value = check_sms_type(item['SMS Type'])
                                term_location_value = check_term_location(item['Term Location'])

                                # print(item)
                                # print("voice_carrier_value", voice_carrier_value)
                                # print("customer_value", customer_value)
                                # print("resller_value", resller_value)
                                # print("service_status_value", service_status_value)
                                # print("service_type_value", service_type_value)
                                # print("sms_carrier_value", sms_carrier_value)
                                # print("sms_type_value", sms_type_value)
                                # print("term_location_value", term_location_value)

                                if not item['DID'] or switch(item['In Method']) == True or voice_carrier_value == True or service_status_value == True or switch(item['SMS Enabled']) == True or sms_carrier_value == True or sms_type_value == True or term_location_value == True or switch(item['E911 Enabled Billed']) == True or customer_value == True or resller_value == True:
                                    error_flag = True
                                    save_data = Did_Error(
                                    did_uuid = item['DID uuid'], 
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
                                    except Exception as e:
                                        messages.warning(request, e)
                                else:
                                    try:
                                        save_data = Did(
                                        did_uuid = item['DID uuid'], 
                                        did = item['DID'] if item['DID'] else None, 
                                        in_method = switch(item['In Method']), 
                                        voice_carrier = voice_carrier_value, 
                                        status = service_status_value, 
                                        # change_date = parse_date(item['Change Date']), 
                                        change_date =  datetime.datetime.now(), 
                                        sms_enabled = switch(item['SMS Enabled']), 
                                        sms_carrier = sms_carrier_value, 
                                        sms_type = sms_type_value, 
                                        sms_campaign = item['SMS Campaign'], 
                                        term_location = term_location_value, 
                                        customer = customer_value, 
                                        reseller = resller_value, 
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
                                        # updated_date_time = parse_datetime(item['Updated Date Time']), 
                                        updated_date_time = datetime.datetime.now(),
                                        updated_by = item['Updated By'], 
                                        )
                                        save_data.save()
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
        try:
            did = Did(
                did = int(request.POST['did']) if request.POST['did'].isdigit() else None,
                customer = Customer.objects.get(id = int(request.POST['customer'])) if request.POST['customer'] else None,
                reseller = Customer.objects.get(id = int(request.POST['reseller'])) if request.POST['reseller'] else None,
                in_method = request.POST['in_method'],
                status = Status.objects.get(id = int(request.POST['status'])) if request.POST['status'] else None,
                change_date = parse_date(request.POST['change_date']),
                voice_carrier = Voice_Carrier.objects.get(id = int(request.POST['voice_carrier'])) if request.POST['voice_carrier'] else None,
                sms_enabled = request.POST['sms_enabled'],
                sms_carrier = SMS_Carrier.objects.get(id = int(request.POST['sms_carrier'])) if request.POST['sms_carrier'] else None,
                sms_type = SMS_Type.objects.get(id = int(request.POST['sms_type'])) if request.POST['sms_type'] else None,
                sms_campaign = request.POST['sms_campaign'],
                term_location = Term_Location.objects.get(id = int(request.POST['term_location'])) if request.POST['term_location'] else None,
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
            
            did.full_clean()

            did.save()
        
        except Exception as e:
            messages.warning(request, e)
        messages.success(request, 'DID was created successfully!')
        return redirect('/did')
    else:
        customers_data = Customer.objects.values_list('id', 'full_name')
        status = Status.objects.all()
        voice_carrier = Voice_Carrier.objects.all()
        sms_carrier = SMS_Carrier.objects.all()
        sms_type = SMS_Type.objects.all()
        term_location = Term_Location.objects.all()
        customers = []
        for item in customers_data:
            customers.append({'id': item[0], 'full_name': item[1]})
        return render(request, 'did_create.html', {'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': sms_carrier, 'sms_type': sms_type, 'term_location': term_location})
    

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
        'did': did['did'],
        'customer': did['customer_id'],
        'reseller': did['reseller_id'],
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
        'service_1': did['service_1'],
        'service_2': did['service_2'],
        'service_3': did['service_3'],
        'service_4': did['service_4'],
        'updated_date_time': did['updated_date_time'] if not did['updated_date_time'] else did['updated_date_time'].strftime('%Y-%m-%d'),
        'updated_by': did['updated_by'],
    }

    customers_data = Customer.objects.values_list('id', 'full_name')
    status = Status.objects.all()
    voice_carrier = Voice_Carrier.objects.all()
    sms_carrier = SMS_Carrier.objects.all()
    sms_type = SMS_Type.objects.all()
    term_location = Term_Location.objects.all()
    customers = []
    for item in customers_data:
            customers.append({'id': item[0], 'full_name': item[1]})

    return render(request, 'did_edit.html', {'did': didData, 'customers': customers, 'status': status, 'voice_carrier': voice_carrier, 'sms_carrier': sms_carrier, 'sms_type': sms_type, 'term_location': term_location})


@login_required
def did_update(request, id):
    did = Did.objects.get(id=id)
    if request.method == "POST":
        try:
            did.did = int(request.POST['did']) if request.POST['did'].isdigit() else None
            did.customer = Customer.objects.get(id = int(request.POST['customer'])) if request.POST['customer'] else None
            did.reseller = Customer.objects.get(id = int(request.POST['reseller'])) if request.POST['reseller'] else None
            did.in_method = request.POST['in_method']
            did.status = Status.objects.get(id = int(request.POST['status'])) if request.POST['status'] else None
            did.change_date = parse_date(request.POST['change_date'])
            did.voice_carrier = Voice_Carrier.objects.get(id = int(request.POST['voice_carrier'])) if request.POST['voice_carrier'] else None
            did.sms_enabled = request.POST['sms_enabled']
            did.sms_carrier = SMS_Carrier.objects.get(id = int(request.POST['sms_carrier'])) if request.POST['sms_carrier'] else None
            did.sms_type = SMS_Type.objects.get(id = int(request.POST['sms_type'])) if request.POST['sms_type'] else None
            did.sms_campaign = request.POST['sms_campaign']
            did.term_location = Term_Location.objects.get(id = int(request.POST['term_location'])) if request.POST['term_location'] else None
            did.user_first_name = request.POST['user_first_name']
            did.user_last_name = request.POST['user_last_name']
            did.extension = int(request.POST['extension']) if request.POST['extension'].isdigit() else None
            did.email = request.POST['email']
            did.onboard_date = parse_date(request.POST['onboard_date'])
            did.note = request.POST['note']
            did.e911_enabled_billed = request.POST['e911_enabled_billed']
            did.e911_cid = int(request.POST['e911_cid']) if request.POST['e911_cid'].isdigit() else None
            did.e911_address = request.POST['e911_address']
            did.service_1 = request.POST['service_1']
            did.service_2 = request.POST['service_2']
            did.service_3 = request.POST['service_3']
            did.service_4 = request.POST['service_4']
            did.updated_date_time = datetime.datetime.now()
            did.updated_by = request.user.username
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
            data = Did.objects.filter(id = int(id)).values()
            writer.writerow([
                data[0]['did'],
                Customer.objects.get(id = data[0]['customer_id']).full_name if data[0]['customer_id'] else "",
                Customer.objects.get(id = data[0]['reseller_id']).full_name if data[0]['reseller_id'] else "",
                data[0]['in_method'],
                Status.objects.get(id = data[0]['status_id']).name if data[0]['status_id'] else "",
                data[0]['change_date'],
                Voice_Carrier.objects.get(id = data[0]['voice_carrier_id']).name if data[0]['voice_carrier_id'] else "",
                data[0]['sms_enabled'],
                SMS_Carrier.objects.get(id = data[0]['sms_carrier_id']).name if data[0]['sms_carrier_id'] else "",
                SMS_Type.objects.get(id = data[0]['sms_type_id']).name if data[0]['sms_type_id'] else "",
                data[0]['sms_campaign'],
                Term_Location.objects.get(id = data[0]['term_location_id']).name if data[0]['term_location_id'] else "",
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
def export_error_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ErrorReport.csv"'
    writer = csv.writer(response)
    writer.writerow(default_header)

    error_data = Did_Error.objects.all().values()
    
    for item in error_data:
        writer.writerow([
            item['did'],
            item['customer'],
            item['reseller'],
            item['in_method'],
            item['status'],
            item['change_date'],
            item['voice_carrier'],
            item['sms_enabled'],
            item['sms_carrier'],
            item['sms_type'],
            item['sms_campaign'],
            item['term_location'],
            item['user_first_name'],
            item['user_last_name'],
            item['extension'],
            item['email'],
            item['onboard_date'],
            item['note'],
            item['e911_enabled_billed'],
            item['e911_cid'],
            item['e911_address'],
            item['did_uuid'],
            item['service_1'],
            item['service_2'],
            item['service_3'],
            item['service_4'],
            item['updated_date_time'],
            item['updated_by'],
            ])
        
    Did_Error.objects.all().delete()
    return response
