from django.shortcuts import render, redirect, HttpResponse
import os

#from django.views.decorators.csrf import csrf_exempt

### Rest Framework ----------------------------------------
from rest_framework.response import Response    # to use DRF function base view
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # to use DRF function base view
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#--- Pandas Library -------------------------------------
from django.http import JsonResponse 
import pandas as pd
import numpy as np
import json


from django.views.generic import TemplateView


# Create your views here.
#☰☰☰ Tracker ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def aCrmModule(request):
    context = {'abc':'abc', }
    return render(request, 'O1_Crm/aCrmModule.html', context)


def aTracker(request):
    dfA = pd.read_csv('data/basInfo.csv')
    Year = str(dfA.loc[0, 'year'])
    
  ### Step 1 - Read Data from CSV File --------------------------------------
  ### =======================================================================
    
    ### if folder is not exsist create the folder first......................
    data_folder = 'Data/'+Year+'/O1_Crm'
    sales_folder = "Meeting"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass


    ### If file not already exist creat and read otherise read the file.........
    file_path = 'Data/'+Year+'/O1_Crm/Meeting/meetingDetail.csv'
    if os.path.isfile(file_path):
        req_cols = ['id','metRef']
        df = pd.read_csv(file_path, usecols=req_cols).fillna(0)
    else:
        # create a new DataFrame with the required columns
        req_cols = ["id", "metRef", "metDat", "cusCode", "cusName", "salCode", "salPer", "priNote", "pubNote", "othNote", "areaLat","areaLon","areaName", "refer", "comment"]
        df = pd.DataFrame(columns=req_cols).fillna(0)
        df.to_csv('Data/'+Year+'/O1_Crm/Meeting/meetingDetail.csv',index=False, mode='a')


    ### check if the dataframe is empty creat a dummy row to start number......
    if df.empty:
        new_row = {'id':int(Year+'0000'), 'metRef':int(Year+'0000')} # create a new dummy row
        df.loc[0] = new_row  # add the new row to the dataframe

    val = df['id'].max()
    lastN  = val+1


    context = {'lastN':lastN, }
    return render(request, 'O1_Crm/aTracker.html', context)


#@csrf_exempt
@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def meetNotes(request):
    #(To Save Tracker list)

    dfA = pd.read_csv('data/basInfo.csv')
    Year = str(dfA.loc[0, 'year'])    

    Data = request.data
    
    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['metRef'], 
              'metRef': Data['metRef'],
              'metDat': Data['metDat'], 
              'cusCode': Data['cusCode'],
              'cusName': Data['cusName'],
              'salCode': '', #Data['salCode'],	
              'salPer': Data['salPer'],	
              'priNote': Data['priNote'],	
              'pubNote': Data['pubNote'],
              'othNote': Data['othNote'],
              'areaLat': Data['areaLat'],
              'areaLon': Data['areaLon'],
              'areaName': Data['areaName'],
              'refer': '',	
              'comment': '',
            }

    ### Create Folder If not Already Exist.............................
    data_folder = 'Data/'+Year+'/O1_Crm'
    sales_folder = "Meeting"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/'+Year+'/O1_Crm/Meeting/meetingDetail.csv',index=False, header=False, mode='a')


    jsonData = {"Refere":Data['metRef'] }
    return JsonResponse(jsonData)



def aMeetingList(request):
    #(To Show all the Meeting Notes Screen)
    context = {'Data':'Data' }
    return render(request, 'O1_Crm/aMeetingList.html', context)



def showMeeting(request):
    #(Get Meeting Information from Excel File to show on Meeting List on Screen)
    
    ### Get Current Year Value -----------------------------------------------------------
    dfA = pd.read_csv('data/basInfo.csv')
    Year = str(dfA.loc[0, 'year']) 

    ###---- Read Customer Master File 'cusCode and cusName' columns --------------------
    req_cols = ['metRef','metDat', 'cusName','salPer', 'priNote','comment']
    df = pd.read_csv('Data/'+Year+'/O1_Crm/Meeting/meetingDetail.csv', usecols=req_cols).fillna(0)


    # remove duplicate rows and keep only the last occurrence subequently if that customer Code added
    DataA = df.drop_duplicates(subset=['metRef'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)


    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



def meetingEdit(request, pk):
    print(pk)
    #(to Show Quotation to edit)

    ### Get Current Year Value -----------------------------------------------------------
    dfA = pd.read_csv('data/basInfo.csv')
    Year = str(dfA.loc[0, 'year']) 

    ###---- Read Customer Master File 'cusCode and cusName' columns --------------------
    df = pd.read_csv('Data/'+Year+'/O1_Crm/Meeting/meetingDetail.csv').fillna(0)


    # remove duplicate rows and keep only the last occurrence subequently if that customer Code added
    # will show because keep last record will not have 'Delete' in comment column
    DataA = df.drop_duplicates(subset=['metRef'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    record = DataB[DataB['metRef'] == int(pk)]


    Data = record.to_dict(orient="records")
    #print(quotAddiItems)

    context = {'Data': Data }
    return render(request, 'O1_Crm/meetingEdit.html', context)
