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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymsteams
import os

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

            s = smtplib.SMTP(os.getenv('SMTP_SERVICE'), os.getenv('EMAIL_PORT'))
            s.starttls()
            s.login(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PASSWORD'))

            client_message_html = f"""\
            <html>
                <body>
                    <p style="font-size:16px">Hello <strong>{request.POST['username']}</strong>.</p>
                    <br>
                    <p><strong>Congratulations🎉,</strong> The service order you requested has been registered correctly.</p>
                    <p>Our support team will review and let you know soon.</p>
                    <br>
                    <p>Thank you.</p>
                    <p style="font-size:16px"><strong>Mobex.</strong></p>
                </body>
            </html>
            """

            server_message_html = f"""\
            <html>
                <body>
                    <p style="font-size:16px">Hello <strong>{request.user.username}</strong>.</p>
                    <br>
                    <p>A new service order was created.</p>
                    <p>Please review the service order and accept it.</p>
                    <br>
                    <p>Here is the detailed information.</p>
                    <p>Requested username: <strong>{request.POST['username']}</strong></p>
                    <p>Requested email: <strong>{request.POST['email']}</strong></p>
                    <p>Requested number: <strong>{request.POST['number']}</strong></p>
                    <p>Requested port date: <strong>{request.POST['requested_port_date']}</strong></p>
                    <p>Requested E911 number: <strong>{request.POST['e911_number']}</strong></p>
                    <p>Requested E911 address: <strong>{request.POST['e911_address']}</strong></p>
                    <p>Requested description: {request.POST['texting']}</p>
                    <p>Thank you.</p>
                </body>
            </html>
            """

            client_message = MIMEMultipart('alternative')
            server_message = MIMEMultipart('alternative')
            client_message.attach(MIMEText(client_message_html, _subtype='html'))
            server_message.attach(MIMEText(server_message_html, _subtype='html'))
            
            client_message["Subject"] = 'Welcome to Mobex Service!'
            client_message["From"] = os.getenv('EMAIL_SERVER')
            client_message["To"] = request.POST['email']

            server_message["Subject"] = 'A new service order has arrived'
            server_message["From"] = request.POST['email']
            server_message["To"] = os.getenv('EMAIL_SERVER')

            s.sendmail(os.getenv('EMAIL_SERVER'), request.POST['email'], client_message.as_string())
            s.sendmail(request.POST['email'], os.getenv('EMAIL_SERVER'), server_message.as_string())
            s.quit()

            post_create_msg = pymsteams.connectorcard(os.getenv('TEAMS_WEBHOOK_URL'))
            post_create_msg.title("A new service order was created.")
            msg_text = f"\nHere is the detailed information.\n Requested username: {request.POST['username']}\n Requested email: {request.POST['email']}\n Requested number: {request.POST['number']}\n"
            msg_text += f" Requested port date: {request.POST['requested_port_date']}\n" if request.POST['requested_port_date'] else ''
            msg_text += f" Requested E911 number: {request.POST['e911_number']}\n" if request.POST['e911_number'] else ''
            msg_text += f" Requested E911 address: {request.POST['e911_address']}\n" if request.POST['e911_address'] else ''
            msg_text += f" Requested description: {request.POST['texting']}\n" if request.POST['texting'] else ''
            post_create_msg.text(msg_text)
            post_create_msg.send()
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
            'texting': service_order.texting,
        }
        return render(request, 'service_order_edit.html', {'service_order': service_order_data})