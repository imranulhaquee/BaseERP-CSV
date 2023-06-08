from django.shortcuts import render, redirect, HttpResponse
import os
import csv

from django.conf import settings  #to save image in disk
from django.core.files.storage import default_storage #to save image in disk

from I1_Hrm.models import empBasic, empExtra

#--- Pandas Library -------------------------------------
from django.http import JsonResponse 
import pandas as pd
import numpy as np
import json


### Rest Framework ----------------------------------------
from rest_framework.response import Response    # to use DRF function base view
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # to use DRF function base view
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


#--- Upload Data or Records -----------------------------
from .resources import empBasicResource, empExtraResource
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload

### Data Base and Serializers ----------------------------
from I1_Hrm.serializers import empBasicSerializer, empExtraSerializer, empInitSerializer

### --- Get Data from DataBse through Pands --------------
import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')


### --- Generate PDF ------------------------------------
from django.template.loader import get_template
from xhtml2pdf import pisa 

# Create your views here.

#☰☰☰ HRM SETUP ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def a1_hrmSetup(request):
    context = {'abc':'abc', }
    return render(request, 'I1_HRM/a1_hrmSetup.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
def a1_hrmSetupURL(request):

   ### Step 1 - Create Main-Folders - "I1_Hrm" ====================
   ### ------------------------------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])  

    mainFolder = "Data/" + Year + "/I1_Hrm"
    os.makedirs(mainFolder, mode=0o777, exist_ok=True)


   ### Step 2 - Create Sub-Folder - "Employee" ====================
   ### ------------------------------------------------------------
    subFolder = "Employees"

    # Create the subfolder within the main folder.......
    subFolder_path = os.path.join(mainFolder, subFolder)
    os.makedirs(subFolder_path, mode=0o777, exist_ok=True)


   ### Step 3.1 - Create CSV file - "empTarget.csv" ==============
   ### -----------------------------------------------------------
    fileName = 'empTarget.csv'
    file_path = os.path.join(mainFolder, subFolder, fileName)

    if not os.path.exists(file_path):
        headers = ['id','empCode','empName','empImg','empPosi','anSalary',
                   'anTarget','empStat','targetSet','traDate','comment']

        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file); 
            writer.writerow(headers)

   ### Step 3.2 - Create CSV file - "empTargetDetail.csv" ========
   ### -----------------------------------------------------------
    fileName = 'empTargetDetail.csv'
    file_path = os.path.join(mainFolder, subFolder, fileName)

    if not os.path.exists(file_path):
        headers = ['id','empCode','empName','anSalary','anTarget',
                  'sNo','itemCode','itemDesc','titemSelPrice','qty','salesTarget',
                  'totalSalCost','salCostPU','traDate','comment']
        
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file); 
            writer.writerow(headers)


    jsonData = {"name": "Ecolab"}
    return JsonResponse(jsonData)




#☰☰☰ Emmployee Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def a3_EmployeeModule(request):
    context = {'abc':'abc', }
    return render(request, 'I1_HRM/a3_EmployeeModule.html', context)




#☰☰☰ Employee Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def mEmpMasterList(request):
    #(Employee Main Page)
    context = {'basData':'basData' }
    return render(request, 'I1_Hrm/mEmpMasterList.html', context)


def mEmpMasterShow(request):
    #(Show the Detail Supplier Information)

  ### Step 1 - Get Company and Year - to Load Data --------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 1. Save Data in EmpMaster.csv file --------------------------------
  ### ========================================================================
    req_cols = ['empCode','empCName','empEmail','empPosi','empDept','empImg', 'empStat', 'action']
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')


    ### Remove Duplicate Delivery and Deleted Record...
    df = df.drop_duplicates(subset=['empCode'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index).fillna('')


  ### Step 3 - Convert Data into Json Dictionary (can be access by JavaScript) --------
    Data = df.to_dict(orient="records")


    ### Return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



def syncEmpMaster(request):

  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read Data in EmpMaster.csv file -------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Delivery and Deleted Record...
    df = df.drop_duplicates(subset=['empCode'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index).fillna('')

    df = df.sort_values(['empCode'], ascending = [True])


  ### Step 3 - Save Data in EmpMaster.csv file -------------------------------
  ### ========================================================================
    statPath =  "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def mEmpMasterAdd(request):
    #(Screen to Add New Cutomer)
    context = {'Data':'Data' }
    return render(request, 'I1_Hrm/mEmpMasterAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def mEmpMasterAddUrl(request):
    Data = request.data
    print(Data['empImg'])

    ###---- Save Image through Python -----------------------------------------
    ###........................................................................
    filename = (Data['empCode'])+" "+(Data['empFName'])+".jpg"
    csvImgPath = "images/empImg/"+filename ### to save in csv File
    image_file = Data['empImg'] ### image file from html form data

    if (image_file) == 'abc': ### from Add html
        csvImgPath = "Empty.jpg"
    elif (image_file) == 'aaa': ### from Edit html
        pass
    else:
      folder_path = os.path.join(settings.MEDIA_ROOT, 'images', 'empImg') #destination folder i.e. media/images/empImg
      os.makedirs(folder_path, exist_ok=True) # Create the directory if it doesn't exist
      file_path = os.path.join(folder_path, filename) # Construct the file path within the destination folder
      with default_storage.open(file_path, 'wb+') as destination:
          destination.write(image_file.read())


  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 1. Get Data and store in variable ---------------------------------
  ### ========================================================================
    EmpCName = (Data['empFName'])+" "+(Data['empMName'])+" "+(Data['empMName'])
    EmpMaster =  {'id': Data['id'], 
                  'empCode': Data['empCode'],
                  'empFName': Data['empFName'], 
                  'empMName': Data['empMName'],
                  'empLName': Data['empLName'] , 
                  'empCName': EmpCName,
                  'empStat': Data['empStat'],
                  'empImg': csvImgPath,
                  'empPosi': Data['empPosi'],	
                  'empDoj': Data['empDoj'],	
                  'empEid': Data['empEid'],	
                  'empLoca': Data['empLoca'],
                  'empDept': Data['empDept'],
                  'empRepTo': Data['empRepTo'],	
                  'empSpon': Data['empSpon'],
                  'empNatl': Data['empNatl'],
                  'empGend': Data['empGend'],	
                  'empDob': Data['empDob'],	
                  'empMarr': Data['empMarr'],
                  'empIban': Data['empIban'],
                  'empBank': Data['empBank'],
                  'empAcc': Data['empAcc'],
                  'empUid': Data['empUid'],
                  'empVisa': Data['empVisa'],
                  'empAdd': Data['empAdd'],
                  'empPh': Data['empPh'],
                  'empEmail': Data['empEmail'],
                  'ref': Data['ref'],
                  'traDate': Data['traDate'],
                  'action': '',
                }


  ### Step 3 - Get Data and store in variable --------------------------------
  ### ========================================================================
    empMaster = pd.DataFrame(EmpMaster, index=[0])
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    empMaster.to_csv(fPath, index=False, header=False, mode='a')


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def mEmpMasterEdit(request, pk):
    pk = int(pk)

  ###---- Standard Code to load Data -----------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 1. Save Data in EmpMaster.csv file --------------------------------
  ### ========================================================================

    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    selEmp = df[df['empCode'] == pk].fillna(0) ### Filter data as per 'pk' selected quote


    ### file doesn't recongnize date formate first convert into date and than strftime
    selEmp['empDoj'] = pd.to_datetime(selEmp['empDoj']).dt.strftime('%Y-%m-%d')
    selEmp['empDob'] = pd.to_datetime(selEmp['empDob']).dt.strftime('%Y-%m-%d')


    ### Remove Duplicate Delivery and Deleted Record...
    selEmp  = selEmp .drop_duplicates(subset=['empCode'], keep='last')
    selEmp  = selEmp .drop(selEmp .loc[df['action']=='Deleted'].index).fillna('')


  ### Step 3 - Convert Data into Json Dictionary -----------------------------
  ### ========================================================================
    Data = selEmp.to_dict(orient="records")


    #(Screen to Add New Cutomer)
    context = {'Data':Data}
    return render(request, 'I1_Hrm/mEmpMasterEdit.html', context)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def mEmpMasterDelete(request, pk):
    pk = int(pk)

  ###---- Standard Code to load Data -----------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])

  ### Step 2 - Save Data in EmpMaster.csv file -------------------------------
  ### ========================================================================
    #pk = 9996
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    selEmp = df[df['empCode'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Delivery and Deleted Record...
    selEmp  = selEmp .drop_duplicates(subset=['empCode'], keep='last')
    selEmp  = selEmp .drop(selEmp .loc[df['action']=='Deleted'].index).fillna('')

    ###..Get 'Employee Staus' and 'Image Root'........................
    empStat = selEmp.loc[selEmp['empCode'] == pk, 'empStat'].values[0]
    empImag = selEmp.loc[selEmp['empCode'] == pk, 'empImg'].values[0]

    print(empImag)

    if (empStat) == 'Inactive': ### Delete if Inactive
      if (empImag) != "Empty.jpg":  ### Handle Image Deletion
          try:
              file_path = os.path.join(settings.MEDIA_ROOT, empImag) ### Get absolute path
              os.remove(file_path)
          except:
              pass

      ### Save the record(dataframe) in csv file---------------
      selEmp['action'] = 'Deleted'       
      fPath = fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
      selEmp.to_csv(fPath, index=False, header=False, mode='a')

      return Response('Items delete successfully!')

    return Response('Unable to delet....!')



@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def empBasInfo(request):
    #(Get Specific column from Customer Basic DataTable)

  ### Step 1 - Get Company and Year - to Load Data --------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 1. Save Data in EmpMaster.csv file --------------------------------
  ### ========================================================================
    req_cols = ['id', 'empCode', 'empFName']
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

  ### Step 3 - Convert Data into Json Dictionary (can be access by JavaScript) --------
    Data = df.to_dict(orient="records")


    ### Return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Employee Target ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def tEmpTargetList(request):
    
  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])
    

  ### Step 2 - Read Employee- salesTarget.csv File ---------------------------
  ### ========================================================================
    req_cols = ['empCode','empCName','empPosi','empImg','anTarget','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

    DataA = df.drop_duplicates(subset=['empCode'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    Data = DataB.to_dict(orient="records")


    context = {'Data':Data }
    return render(request, 'I1_Hrm/tEmpTargetList.html', context)



def syncEmpTarget(request):

  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read Employee- salesTarget.csv File ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    df['unique'] = df['empCode'].astype(str)+" "+df['sNo'].astype(str) ### create a unique column

    DataA = df.drop_duplicates(subset=['unique'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    DataB = DataB.sort_values(['empCode','sNo'], ascending = [True,True])


  ### Step 3 - Save Data in salesTarget.csv file -----------------------------
  ### ========================================================================
    statPath =  "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    DataB.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def tEmpTargetAdd(request):
    #(To Set Employee Sales Target)

  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Create a List of Employees- whose target has already been set--
  ### ========================================================================
    req_cols = ['empCode','sNo','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')
    
    df['unique'] = df['empCode'].astype(str)+" "+df['sNo'].astype(str) ### create a unique column

    DataA = df.drop_duplicates(subset=['unique'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    uList = DataB['empCode'].unique() ### create a unique array
    List = uList.tolist()  ### convert array to list

    context = {'List':List }
    return render(request, 'I1_Hrm/tEmpTargetAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def tEmpTargetURL(request):
    #(To Save detail Sales Target)

  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])

   
    addiData = request.data
    addRecords = []
    for Data in addiData:
        #Variable to Save in CSV File ..........
        Addi  = { 'id':	Data['empCode'],
                  'empCode':	Data['empCode'], 
                  'empCName':	Data['empName'],
                  'empImg': Data['image'],
                  'empPosi': Data['empPosi'],
                  'anSalary':	Data['anSalary'], 
                  'anTarget':	Data['anTarget'], 
                  'empStat' : 'Active',
                  'targetSet' : 'Yes',
                  'sno':	Data['sno'],
                  'itmcode':	Data['itmcode'],
                  'desc':	Data['itmdesc'],
                  'itemselprice': Data['itemselprice'],
                  'qty':	Data['qty'],
                  'salestarget':	Data['salestarget'],
                  'totalsalcost':	Data['totalsalcost'],
                  'salcostpu':	Data['salcostpu'],
                  'traDate':	Data['traDate'],   
                  'action':	Data['action'], 
                }
        addRecords.append(Addi)  # Add the dictionary to the list
    
    dfAddi = pd.DataFrame(addRecords)
    dfAddi.to_csv("Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv",index=False, header=False, mode='a')

    jsonData = {"Refere":Data['empCode'] }
    return JsonResponse(jsonData)


def tEmpTargetEdit(request, pk):
    pk = int(pk)
    #(To Set Employee Sales Target)

  ##----DEFAULT INFORMATION--------------------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])   
  ##----DEFAULT INFORMATION--------------------------------------------------


  ### Step 2 - Read Employee- salesTarget.csv File --------------------------
  ### -----------------------------------------------------------------------
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    #pk = 345
    df = df[df['empCode'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    df['unique'] = df['empCode'].astype(str)+" "+df['sNo'].astype(str) ### create a unique column

    DataA = df.drop_duplicates(subset=['unique'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    Data = DataB.to_dict(orient="records")

    context = {'Data':Data }
    return render(request, 'I1_Hrm/tEmpTargetEdit.html', context)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def tEmpTargetDelete(request, pk):
    pk = int(pk)

  ###---- Standard Code to load Data -----------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read Employee- salesTarget.csv File ---------------------------
  ### ========================================================================
    #pk = 709
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    df = df[df['empCode'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    df['unique'] = df['empCode'].astype(str)+" "+df['sNo'].astype(str) ### create a unique column

    DataA = df.drop_duplicates(subset=['unique'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    DataB = DataB.drop('unique', axis=1)
    
    DataB['action'] = 'Deleted'


  ### Step 3 - Save Data in salesTarget.csv file -----------------------------
  ### ========================================================================
    ### Save the record(dataframe) in csv file
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    DataB.to_csv(fPath, index=False, header=False, mode='a')


    return Response('Deleted successfully....!')




#☰☰☰ EMPLOYEE SALARY DETAIL ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def empSalary(request):
    #(Show the Detail Supplier Information)

  ### Step 1 - Get Company and Year - to Load Data ---------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read Employee- salesTarget.csv File ---------------------------
  ### ========================================================================
    req_cols = ['empCode' ,'empCName', 'empPosi', 'empImg', 'action']
    fPath = "Data/" +coFolder+ "/I1_Hrm/EmpMaster.csv"
    dfDetail = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

    DataA = dfDetail.drop_duplicates(subset=['empCode'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record

    DataB = DataB.fillna('')
    iniData = DataB[['empCode','empCName','empPosi', 'empImg']]


  ### Step 2 - Read Employee- salesTarget.csv File ---------------------------
  ### ========================================================================
    Data = iniData.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Upload Trial Balance ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def zUploadEmpData(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_itmBasic = request.FILES['myfile']

        if not new_itmBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_itmBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              value = empBasic(data [0], data [1], data [2], data [3], data [4], data [5],)
              value.save()

              value2 = empExtra(data [0], data [1], data [6], data [7], data [8], data [9],data [10],
                                data [11], data [12], data [13], data [14],data [15], data [16],
                                data [17], data [18], data [19], data [20],data [21],data [22],
                                data [23], data [24], data [25], data [26])
              value2.save()
            
        messages.info(request,'Upload Successfully')

    return render(request, 'I1_Hrm/zUploadEmpData.html')

