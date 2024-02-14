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


@login_required
def service_order_list(request):
    service_orders = Service_Order.objects.all()
    return render(request, 'service_orders.html', {'service_orders': service_orders})