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

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def list(request):
    dids_list = Did.objects.all()
    paginator = Paginator(dids_list, 5)
    page = request.GET.get('page')
    try:
        dids = paginator.page(page)
    except PageNotAnInteger:
        dids = paginator.page(1)
    except EmptyPage:
        dids = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'dids': dids})
# Create your views here.
