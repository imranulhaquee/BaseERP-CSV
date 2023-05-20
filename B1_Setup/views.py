from django.shortcuts import render, redirect
from A1_Admin.models import Accounts
from B1_Setup.models import stdGrouping

from django.contrib import messages, auth
from tablib import Dataset
from django.db import transaction
from B1_Setup.resources import stdGroupingResource


#--- Pandas Library -------------------------------------
from django.http import JsonResponse 
import pandas as pd
import numpy as np
import json



def home(request):

    context = {'abc':'abc', }
    return render(request, 'home.html', context)

  
def LP(request):

    user = request.user
    if Accounts.objects.filter(id= user.id, access="BaseERP"):
        #pass
        context = {'abc':"get the variables", }
        return render(request, 'B1_Setup/LP.html', context)
    else:
        return redirect('login')


###----------- Chart of Accounts ----------------------------------------



def UploadStdGrouping(request):
   #--Ensure that use is Supplier to show "Supplier Dashboard"--------------
    user = request.user
    if Accounts.objects.filter(id= user.id, access="BaseERP"):
        pass
    else:
        return redirect('login')

    if request.method == 'POST':
        options_resouce = stdGroupingResource()
        dataset = Dataset()
        new_options = request.FILES['myfile']

        if not new_options.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_options.read(),format='xlsx')
        for data in imported_data:
            value = stdGrouping(data [0], data [1], data [2], data [3], data [4], data [5], data [6],)
            value.save()

        messages.info(request,'Upload Successfully')
    return render(request,'B1_Setup/UploadStdGrouping.html')
