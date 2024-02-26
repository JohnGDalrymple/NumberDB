from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
import pandas as pd
from operator import or_
import smtplib

# Create your views here.

def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y').date() if date_string else None

default_data_header = ['username', 'email', 'number', 'texting', 'e911_number', 'e911_address']

def switchStatus(value):
    if value == 0:
        return 'Created'
    elif value == 1:
        return 'Updated'
    elif value == 2:
        return 'Deleted'
    elif value.lower() == 'created':
        return 0
    elif value.lower() == 'updated':
        return 1
    elif value.lower() == 'deleted':
        return 2
    else:
        return None


@login_required
def service_order_list(request):
    service_orders = []
    if request.GET.get('search'):
        query = request.GET['search']
        q_objects = Q()
        for field in default_data_header:
            q_objects |= Q(**{field + '__icontains': query})

        service_orders = Service_Order.objects.filter(q_objects)

        for item in service_orders:
            item.username = "" if(item.username == None) else item.username
            item.email = "" if(item.email == None) else item.email
            item.requested_port_date = "" if(item.requested_port_date == None) else item.requested_port_date.strftime('%Y-%m-%d')
            item.number = "" if(item.number == None) else item.number
            item.texting = "" if(item.texting == None) else item.texting
            item.status = switchStatus(item.status)
            item.e911_address = "" if(item.e911_address == None) else item.e911_address
            item.e911_number = "" if(item.e911_number == None) else item.e911_number

        size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(service_orders, size)
        service_list = paginator.get_page(page_number)

        return render(request, 'service_orders.html', {'service_orders': service_list, 'search': query})
    else:
        service_orders = Service_Order.objects.all()
        
        for item in service_orders:
            item.username = "" if(item.username == None) else item.username
            item.email = "" if(item.email == None) else item.email
            item.requested_port_date = "" if(item.requested_port_date == None) else item.requested_port_date
            item.number = "" if(item.number == None) else item.number
            item.texting = "" if(item.texting == None) else item.texting
            item.status = switchStatus(item.status)
            item.e911_address = "" if(item.e911_address == None) else item.e911_address
            item.e911_number = "" if(item.e911_number == None) else item.e911_number

        size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(service_orders, size)
        service_list = paginator.get_page(page_number)

        return render(request, 'service_orders.html', {'service_orders': service_list})


@login_required
def service_order_delete(request, id):
    try:
        service_order = Service_Order.objects.get(id=id)
        service_order.status = 2
        service_order.save()
        messages.warning(request, 'The service order was deleted successfully!')
    except Exception as e:
        messages.warning(request, e)
    return redirect('/service_order')


@login_required
def service_order_add(request):
    if request.method == 'POST':
        try:
            service_order = Service_Order(
                username = request.POST['username'],
                email = request.POST['email'],
                number = int(request.POST['number']),
                requested_port_date = parse_date(request.POST['requested_port_date']),
                texting = request.POST['texting'],
                e911_address = request.POST['e911_address'],
                e911_number = int(request.POST['e911_number']) if request.POST['e911_number'] else None,
                )
            service_order.full_clean()
            service_order.save()

            # sender = 'ginik0108@gmail.com'
            # receivers = ['comsuper0030@gmail.com']
            # message = """From: From Person <from@example.com>
            # To: To Person <comsuper0030@gmail.com>
            # Subject: SMTP email example


            # This is a test message.
            # """

            # try:
            #     smtpObj = smtplib.SMTP('localhost')
            #     smtpObj.sendmail(sender, receivers, message)         
            #     print("Successfully sent email")
            # except Exception:
            #     pass
        except Exception as e:
            messages.warning(request, e)

        messages.success(request, 'The service order was created successfully!')
        return redirect('/service_order')
    else:
        return render(request, 'service_order_create.html')
    

@login_required
def service_order_update(request, id):
    service_order = Service_Order.objects.get(id=id)
    if request.method == "POST":
        try:
            service_order.username = request.POST['username']
            service_order.email = request.POST['email']
            service_order.number = request.POST['number']
            service_order.requested_port_date= parse_date(request.POST['requested_port_date'])
            service_order.texting = request.POST['texting']
            service_order.e911_address = request.POST['e911_address']
            service_order.e911_number = int(request.POST['e911_number']) if request.POST['e911_number'] else None
            service_order.updated_at = datetime.datetime.now()
            service_order.status = 1
            service_order.full_clean()
            service_order.save()
            messages.success(request, 'The service order was updated successfully!')
        except Exception as e:
            messages.warning(request, e)
        return redirect('/service_order')
    else:
        service_order_data = {
            'id': service_order.id,
            'username': service_order.username,
            'email': service_order.email,
            'number': service_order.number,
            'status': switchStatus(service_order.status),
            'requested_port_date': service_order.requested_port_date.strftime('%Y-%m-%d'),
            'e911_number': service_order.e911_number,
            'e911_address': service_order.e911_address,
        }
        return render(request, 'service_order_edit.html', {'service_order': service_order_data})