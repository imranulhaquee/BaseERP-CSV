from django.shortcuts import render, redirect, HttpResponse
import os


from F1_Sales.models import cusBasic, cusExtra, qotBasic, qotAddi, soBasic, soAddi, dlBasic, dlAddi, siBasic, siAddi
from H1_Items.models import  itmLedger

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
from .resources import cusBasicResource, cusExtraResource
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload

### Data Base and Serializers ----------------------------
from F1_Sales.serializers import cusBasicSerializer, cusExtraSerializer, cusInitSerializer,qotBasicSerializer, qotAddiSerializer, soBasicSerializer, soAddiSerializer, dlBasicSerializer, dlAddiSerializer, siBasicSerializer, siAddiSerializer

### --- Get Data from DataBse through Pands --------------
import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')

### --- Generate PDF ------------------------------------
from django.template.loader import get_template
from xhtml2pdf import pisa 


# from django.template import RequestContext

#☰☰☰ SALES DASHBOARD ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def a2_salesDB(request):
    context = {'abc':'abc', }
    return render(request, 'F1_Sales/a2_salesDB.html', context)




#☰☰☰ SALES SETUP ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def a1_salSetup(request):
    context = {'abc':'abc', }
    return render(request, 'F1_Sales/a1_salSetup.html', context)



#☰☰☰ SALES Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aSalesModule(request):
    context = {'abc':'abc', }
    return render(request, 'F1_Sales/aSalesModule.html', context)



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Customer Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aCustomers(request):
    #(Customer Main Page)
    context = {'basData':'basData' }
    return render(request, 'F1_Sales/aCustomers.html', context)


def aCusRefresh(request):

  ### Step 1 - Read Data from SQL--------------------------------------------
  ### =======================================================================
    basic = pd.read_sql('''SELECT * FROM "F1_Sales_cusBasic" ''', con=engine)
    Extra = pd.read_sql('''SELECT * FROM "F1_Sales_cusExtra" ''', con=engine)


  ### Step 2 - Merge "Basic & Extra" Dataframe by Customer ID----------------
  ### =======================================================================
    Combined = pd.merge(basic, Extra, on=["cusCode"])
    Combined = Combined.drop("id_y", axis=1)
    Combined = Combined.rename(columns={'id_x': 'id'})

    Combined['comment'] = ''


  ### Step Step 3 - Create a "Customer" Folder inside "Data/F1_Sales" Folder-
  ### =======================================================================
    data_folder = "Data/F1_Sales"
    sales_folder = "Customer"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass


  ### Step 4 - Save Customer Master File as CSV File ------------------------
  ### =======================================================================
    #https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
    Combined.to_csv('Data/F1_Sales/Customer/CustMaster.csv',index = False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def cusListURL(request):
    ### Step 1- Read CSV Files in Pandas......................................
    ### ----------------------------------------------------------------------
    req_cols = ['cusCode','cusName', 'comment','cusBillTo','cusShipTo']
    fPath = "Data/F1_Sales/Customer/CustMaster.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna(0)

    ### Step 1a- Remove Duplicate Line and Deleted Record...............
    df = df.drop_duplicates(subset=['cusCode'], keep='last')
    df = df.drop(df.loc[df['comment']=='Delete'].index)

    ### Step 1b- Remove Duplicate Line and Deleted Record...............
    Data = df.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 


def showCust(request):  #delete after ensure that customer list is working properly
    #(Show the Detail Customer Information)

    ### Read CSV Files in Pandas...........................
    df = pd.read_csv("Data/F1_Sales/Customer/CustMaster.csv").fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = df.drop_duplicates(subset=['cusCode'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ### Convert Data into Json Dictionary..................
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def cusSelInfo(request):
    #(Get Specific Column from Excel file and convert into Json)

    ###---- Qutation File to Get Last Quotation Number -------------
    req_quot = ['qotRef']
    dfQuot = pd.read_csv("Data/F1_Sales/Quotation/salQuot2023.csv", usecols=req_quot)
    lastQuot = dfQuot['qotRef'].max()

    ###---- Customer Master File to Get Last Quotation Number -------------
    req_cols = ['cusCode','cusName', 'cusBillTo','cusShipTo', 'comment']
    df = pd.read_csv("Data/F1_Sales/Customer/CustMaster.csv", usecols=req_cols).fillna(0)

    # remove duplicate rows and keep only the last occurrence subequently if that customer Code added
    # will show because keep last record will not have 'Delete' in comment column
    DataA = df.drop_duplicates(subset=['cusCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)
    DataB = DataB.drop('comment', axis=1)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def lastQuot(request):
    ###---- Read the Standard File to get Year ---------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    
    ###---- Qutation File to Get Last Quotation Number -------------   
    try: 
        req_cols = ['qotRef', 'qotDat']
        fPath = "Data/"+Year+"/F1_Sales/Quotations/"+qotBasic
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'qotRef': [0]}
        df = pd.DataFrame(data)
    
    ### Step 1a - Get the last Quotation No make it 5 digit and add year ------
    maxValue = df['qotRef'].max()
    maxValue = str(maxValue + 1)
    number = maxValue.rjust(5, "0")
    lastQuot = str(Year[2:]) + str(number)
    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return Response(lastQuot) 


@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def cusBasInfo(request):
    #(Get Specific column from Customer Basic DataTable)

    Detail = cusBasic.objects.only('id', 'cusCode', 'cusName') 
    serilizer = cusInitSerializer(Detail, many=True)
    return Response(serilizer.data)



def addCustomer(request):
    #(Screen to Add New Cutomer)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/addCustomer.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def addCust(request):
    Data = request.data
    
    #---- Customer Basic Information ---------------------------------------
    customerBasic = cusBasic (Data['id'], Data['cusCode'],Data['cusName'],
                              Data['opeBal'], 0 , Data['cusActive'],)
    customerBasic.save()

    #---- Customer Extra Information ---------------------------------------
    customerExt = cusExtra (  Data['id'], Data['cusCode'], Data['cusLogo'], Data['cusPhone'], 
                              Data['cusEmail'], Data['cusWeb'], Data['cusBillTo'], 
                              Data['cusShipTo'], Data['cusAcNum'], Data['cusCrLim'], 
                              Data['cusPytTerm'], Data['cusBank'], Data['cusLegName'], 
                              Data['cusTRN'], Data['cusTP'], Data['cusTOJ'], 
                              Data['cusCP'], Data['cusCPN'],
                            )
    customerExt.save()

    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'cusCode': Data['cusCode'],
              'cusName': Data['cusName'], 
              'opeBal': Data['opeBal'],
              'cloBal':0 , 
              'cusActive': Data['cusActive'],
              'cusLogo': '',
              'cusPhone': Data['cusPhone'],	
              'cusEmail': Data['cusEmail'],	
              'cusWeb': Data['cusWeb'],	
              'cusBillTo': Data['cusBillTo'],
              'cusShipTo': Data['cusShipTo'],
              'cusAcNum': Data['cusAcNum'],	
              'cusCrLim': Data['cusCrLim'],
              'cusPytTerm': Data['cusPytTerm'],
              'cusBank': Data['cusBank'],	
              'cusLegName': Data['cusLegName'],	
              'cusTRN': Data['cusTRN'],
              'cusTP': Data['cusTP'],
              'cusTOJ': Data['cusTOJ'],
              'cusCP': Data['cusCP'],
              'cusCPN': Data['cusCPN'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/F1_Sales/Customer/CustMaster.csv',index=False, header=False, mode='a')
    #df.to_csv('Data/F1_Sales/Customer/tempCust.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def aEditCustomer(request, pk):

    CusBasic = cusBasic.objects.get(id=pk)
    CusExtra = cusExtra.objects.get(id=pk)
    #print(CusBasic.cusCode)

    serBasic = cusBasicSerializer(CusBasic, many=False)
    serExtra = cusExtraSerializer(CusExtra, many=False)
    #print(serExtra.data)

    #creates a new dictionary with the same keys as the "serializer.data" dictionary, but with any None values replaced by empty strings.
    ser_Basic = {k: '' if v is None else v for k, v in serBasic.data.items()}
    ser_Extra = {k: '' if v is None else v for k, v in serExtra.data.items()}

    #(Screen to Add New Cutomer)
    context = {'DataA':ser_Basic, 'DataB':ser_Extra,}
    return render(request, 'F1_Sales/aEditCustomer.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def editCus(request):
    
    Data = request.data
    emp = cusExtra.objects.get(id=Data['id'])
    #print(Data)
    
    #---- Customer Basic Information ---------------------------------------
    customerBasic = cusBasic (Data['id'], Data['cusCode'],Data['cusName'],
                              Data['opeBal'], 0 , Data['cusActive'],)
    customerBasic.save()



    #---- Customer Extra Information ---------------------------------------
    customerExt = cusExtra (  Data['id'], Data['cusCode'], Data['cusLogo'], Data['cusPhone'], 
                              Data['cusEmail'], Data['cusWeb'], Data['cusBillTo'], 
                              Data['cusShipTo'], Data['cusAcNum'], Data['cusCrLim'], 
                              Data['cusPytTerm'], Data['cusBank'], Data['cusLegName'], 
                              Data['cusTRN'], Data['cusTP'], Data['cusTOJ'], 
                              Data['cusCP'], Data['cusCPN'],
                          )


    img = Data['cusLogo'] #will return sting incase of no img data
                                    
    if (img) == emp.cusLogo: 
        print("image didn't changed...............")
        pass
    else:
      try:
          print("image changed...............")
          os.remove(emp.cusLogo.path)
      except:
          pass

    customerExt.save()


    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'cusCode': Data['cusCode'],
              'cusName': Data['cusName'], 
              'opeBal': Data['opeBal'],
              'cloBal':0 , 
              'cusActive': Data['cusActive'],
              'cusLogo': '',
              'cusPhone': Data['cusPhone'],	
              'cusEmail': Data['cusEmail'],	
              'cusWeb': Data['cusWeb'],	
              'cusBillTo': Data['cusBillTo'],
              'cusShipTo': Data['cusShipTo'],
              'cusAcNum': Data['cusAcNum'],	
              'cusCrLim': Data['cusCrLim'],
              'cusPytTerm': Data['cusPytTerm'],
              'cusBank': Data['cusBank'],	
              'cusLegName': Data['cusLegName'],	
              'cusTRN': Data['cusTRN'],
              'cusTP': Data['cusTP'],
              'cusTOJ': Data['cusTOJ'],
              'cusCP': Data['cusCP'],
              'cusCPN': Data['cusCPN'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/F1_Sales/Customer/CustMaster.csv',index=False, header=False, mode='a')
    #df.to_csv('Data/F1_Sales/Customer/tempCust.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delCus(request, pk):

  #----------Delete Record -----------------------------------------------
    CusBasic = cusBasic.objects.get(id=pk)
    CusExtra = cusExtra.objects.get(id=pk)

    if (CusBasic.opeBal) == '':
        CusBasic.opeBal = 0

    # if ther is any balance in either Opening and closing customer will not delete
    if (CusBasic.opeBal) == 0 and CusBasic.cloBal == 0:
      #----------Handle Image Deletion -------------------------------------
      if (CusExtra.cusLogo) != "Blank.jpg":
          try:
              os.remove(CusExtra.cusLogo.path)
          except:
              pass


      CusBasic.delete()
      CusExtra.delete()

      #Variable to Save in CSV File ..........
      tempDf = {'id': pk, 
                'cusCode': pk,
                'cusName': '', 
                'opeBal': '',
                'cloBal': '' , 
                'cusActive':'',
                'cusLogo': '',
                'cusPhone': '',	
                'cusEmail': '',	
                'cusWeb': '',	
                'cusBillTo': '',
                'cusShipTo': '',
                'cusAcNum': '',	
                'cusCrLim': '',
                'cusPytTerm': '',
                'cusBank': '',	
                'cusLegName': '',	
                'cusTRN': '',
                'cusTP': '',
                'cusTOJ': '',
                'cusCP': '',
                'cusCPN': '',
                'comment': 'Delete',
              }

      df = pd.DataFrame(tempDf, index=[0])
      df.to_csv('Data/F1_Sales/Customer/CustMaster.csv',index=False, header=False, mode='a')
      
      return Response('Items delete successfully!')

    return Response('Unable to delet....!')



def zUploadCusData(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_cusBasic = request.FILES['myfile']

        if not new_cusBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_cusBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              value = cusBasic(data [0], data [1], data [2], data [3], data [4], data [5],)
              value.save()

              value2 = cusExtra(data [0], data [1], data [6], data [7], data [8], data [9],data [10],
                                data [11], data [12], data [13], data [14],data [15], data [16],
                                data [17], data [18], data [19], data [20],data [21],)
              value2.save()
            
        messages.info(request,'Upload Successfully')

    return render(request, 'F1_Sales/zUploadCusData.html')




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Quotation ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sQuotList(request):
    #(To Show all the Quotation Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sQuotList.html', context)


def showQuot(request): #URL to fetch data--

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv File -----------------------------------------
  ### ========================================================================
    req_cols = ['id','qotRef','qotDat','cusName', 'qotTax', 'qotTAT','spCName','opnClo','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('0')
    
    ### drop first row which is empty...
    df = df.drop(df.index[0])

    ### file doesn't recongnize date formate first convert into date and than strftime...
    df['qotDat'] = pd.to_datetime(df['qotDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    df = df.drop_duplicates(subset=['qotRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index)   


  ### Step 3. Read qotStat.csv File ------------------------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['qotRefSt'], keep='last')  ##Drop Duplicate


  ### Step 4 - Map qotBasic.csv Open/Close with qotStat.csv ------------------
  ### ========================================================================
    opnClo_map = dict(zip(stat['qotRefSt'], stat['opnCloSt']))
    df['opnClo'] = df['qotRef'].map(opnClo_map).fillna(df['opnClo'])


  ### Step 5 - Convert Data into Dictionary ----------------------------------
  ### ========================================================================
    Data = df.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 


def syncQuot(request): #URL to fetch data--

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv File - to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfA.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic = dfBasic.sort_values('qotRef') #sor by qotRef

    ### Save the data in qotBasic.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfBasic.to_csv(fPath, index=False)

    dfBasic['unique'] = dfBasic['qotRef'].astype(str)+" "+dfBasic['traDate']

  ### Step 3. Read qotAddi.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfB["unique"] = dfB['qotRef'].astype(str)+" "+dfB['traDate']

    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    merged_df = pd.merge(dfB, dfBasic['unique'], on='unique', how='inner')
    ###---- Rearange Column to aboid any mistake
    merged_df = merged_df[['id','qotRef','sno','itmCod','desc','qty','price','disc','tot','vat','traDate','action']]

    ### Save the data in qotAddi.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    merged_df.to_csv(fPath, index=False)


  ### Step 4. Read qotStat.csv File - to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    stat = stat.drop_duplicates(subset=['qotRefSt'], keep='last')
    stat = stat.drop(stat.loc[stat['action']=='Deleted'].index)


    ### Save the data in qotStat.csv File...
    statPath =  "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    stat.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sQuotAdd(request):

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 1. Read qotBasic.csv - to Get the last Quotation Number -----------
  ### ========================================================================
    try: 
        req_cols = ['qotRef', 'qotDat']
        fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'qotRef': [0]}
        df = pd.DataFrame(data)
    
    ### Get the last Quotation Number and make it 5 digit and add year...
    lastQuot = df['qotRef'].max()


    context = {'lastQuot': lastQuot }
    return render(request, 'F1_Sales/sQuotAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sQuotAddUrl(request):

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])

 
  ### Step 2. Save Data in qotBasic.csv file----------------------------------
  ### ========================================================================
    basData = request.data[0]
    basicData = {'ID': basData['qotRef'],    'qotRef': basData['qotRef'],
              'qotDat': basData['qotDat'],   'cusCode': basData['cusCode'],
              'cusName': basData['cusName'], 'qotTBD':basData['qotTBD'], 
              'qotTAD': basData['qotTAD'],   'qotTax': basData['qotTax'],
              'qotTAT': basData['qotTAT'],	 'shipTo':  basData['shipTo'],	
              'qotComm': basData['qotComm'], 'spCode': basData['spCode'],
              'spCName': basData['spCName'],   'opeClo': 'Open',
              'traDate': basData['traDate'], 'action': basData['action']
            }

    dfBasic = pd.DataFrame(basicData, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3. Save Data in qotAddi.csv file-----------------------------------
  ### ========================================================================
    addiData = request.data[1]
    for data in addiData:
      addiData={'ID': basData['qotRef'], 'qotRef': basData['qotRef'], 'sno':data['sno'],
              'itmCod':data['itmcode'], 'desc':data['desc'], 'qty':data['qty'],
              'price':data['price'], 'disc':data['disc'], 'tot':data ['tot'],
              'vat':data ['vat'], 'traDate':basData['traDate'], 'action':'' 
              }
    
      dfAddi = pd.DataFrame(addiData, index=[0])
      fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
      dfAddi.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 4. Save Data in qotStat.csv file-----------------------------------
  ### ========================================================================
    basData = request.data[0]
    QotStat =  {'qotRef':basData['qotRef'],
                'opnClo':"Open",
                'traDate':basData['traDate'],
                'action':" ",
    }

    dfBasic = pd.DataFrame(QotStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sQuotEdit(request, pk):
    pk = int(pk)
    
  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])

 
  ### Step 2. Save Data in qotBasic.csv file----------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfBasic = dfA[dfA['qotRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['qotDat'] = pd.to_datetime(dfBasic['qotDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in qotAddi
    List = dfBasic["traDate"] #.tolist()

    ### Convert Transaction Date to list to filter records in qotAddi
    quotBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3 - Read qotAddi.csv File------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfAddi = dfB[dfB['qotRef'] == pk].fillna(0) ### Filter as per 'pk' selected quote
    filtered_df = dfAddi[dfAddi['traDate'].isin(List)] ### Filter by transaction Date

    ### Convert Transaction Date to list to filter records in qotAddi
    quotAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary


    context = {'lastQuot': pk, 'qBasic':quotBasi,  'addiQuote':quotAddiItems}
    return render(request, 'F1_Sales/sQuotEdit.html', context)


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delQot(request, pk):
    pk = int(pk)
    
  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])

  ### CHECK - Before Deleting Record ----------------------------------------
    req_cols = ["soRef","qotRef", "action"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')
    dfA = dfA.drop_duplicates(subset=['qotRef'], keep='last') ### Remove Duplicate Record
    dfA = dfA.drop(dfA.loc[dfA['action']=='Deleted'].index)  ### Remove Deleted Record
    list = dfA['qotRef'].tolist() ### Convert Column in LIst
    if pk in list:
        return JsonResponse({'result': 'No'})


  ### Step 2. Read qotBasic.csv File - to Get all the Sales Quotations -------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfBasic = df[df['qotRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    dfBasic['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3.Read qotStat.csv File - to Get all the Sales Quotations ---------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    df_Stat = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    df_Stat = df_Stat[df_Stat['qotRefSt'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    df_Stat['action'] = "Deleted"

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    df_Stat.to_csv(fPath, index=False, header=False, mode='a')


    return Response('Items delete successfully!')


def sQuotPdf(request):
  #----------Get Data from html Page and convert into list---------------
    pk1 = request.GET.get('query_name')
    pk = int(pk1)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv File - to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfBasic = dfA[dfA['qotRef'] == pk].fillna(0) ### Filter

    ###....Step 1a - Remove Duplicate Quote and Deleted Record.........
    dfBasic = dfBasic.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    ###....Step 1b - Combine Employee Code and Transaction Time.......
    List = dfBasic["traDate"] #.tolist()

    quotBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3. Read qotAddi.csv File - to get Quotation Detail ----------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfAddi = dfB[dfB['qotRef'] == pk].fillna(0) ### Filter Record as per 'pk' selected Quote

    ### Filtere the 'Qutation' by Quotation "Target List"
    filtered_df = dfAddi[dfAddi['traDate'].isin(List)]
    quotAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary

  ###--- If Want to see the Formation on Page before taking as pdf------
    #context = {"quotBasi": quotBasi, "quotAddi":quotAddiItems }
    #return render(request, 'F1_Sales/sQuotPdf.html', context)
  ###--- If Want to see the Formation on Page before taking as pdf------

    template_path = "../templates/F1_Sales/sQuotPdf.html"  #template to access
    context = {"quotBasi": quotBasi, "quotAddi":quotAddiItems }   # context is to pass data to html page before converting to PDF

    ###Create a Django response Object, and specify content_type as pdf
    ###---------------------------------------------------------------- 
    response = HttpResponse(content_type='application/pdf')  #normal django response
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'  #pdf to download - 'attachment' if comment out pdf will show on screen
    #response['Content-Disposition'] = 'filename="report.pdf"'  #pdf to download - 'attachment'

    ###Find the template and render it.(its a standard)..
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors')

    return response


def showQuotSum(request): ### didn't find the reason....................
    ###---- Read Quotation File 'with Specific Column' -----------------
    req_cols = ['qotRef','qotDat', 'cusCode', 'cusName', 'opnClo', 'comment']
    dfSal = pd.read_csv("Data/F1_Sales/Quotation/salQuot2023.csv", usecols=req_cols).fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = dfSal.drop_duplicates(subset=['qotRef'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Deleted'].index)
    DataB = DataB.drop('comment', axis=1)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Quotation -COST ☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sQotCotAdd(request, pk):
    
  ###---- Standard Code to load Data -----------------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 1 - Read Item Salece Price----------------------------------------
    req_Column = ['itmCode', 'uPrice']
    SP = pd.read_csv("Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/ItemSalPrice.csv", usecols=req_Column ,encoding='unicode_escape').fillna(0)
    SP = SP.drop_duplicates(subset=['itmCode'], keep='last')
    SP = SP.to_dict(orient="records")   ### Convert Data into Dictionary
    SPList = {item['itmCode']: item['uPrice'] for item in SP} # Extract desired values into a new dictionary


  ### Step 2 - Read Sales Quotation Basic - "F1_Sales (Sales Module)" -------
    pk = int(pk)
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfBasic = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfBasic[dfBasic['qotRef'] == pk].fillna(0) ### Filter

    ###..Remove Duplicate Quote and Deleted Record...........................
    dfBasic = dfBasic.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['qotDat'] = pd.to_datetime(dfBasic['qotDat']).dt.strftime('%Y-%m-%d')

    ###..Get 'Employee Code' and 'Transaction Date...........................
    traDate = dfBasic.loc[dfBasic['qotRef'] == pk, 'traDate'].values[0]
    empCode = dfBasic.loc[dfBasic['qotRef'] == pk, 'spCode'].values[0]

    ###..Convert into List...................................................
    qotBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3 - Read Employee Cost - "I1_Hrm (HRM Module)"--------------------
    req_Column = ['empCode', 'itemCode', 'salCostPU']
    empCost = pd.read_csv("Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv", usecols=req_Column ,encoding='unicode_escape').fillna(0)
    empCost = empCost.loc[empCost['empCode'] == empCode]
    empCost = empCost.to_dict(orient="records")   ### Convert Data into Dictionary
    empCostList = {item['itemCode']: item['salCostPU'] for item in empCost} # Extract desired values into a new dictionary


  ### Step 4 - Read Sales Quote Additional CSV files ------------------------

    ###..Read Quotation Additional CSV File .................................
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfB = dfB[dfB['qotRef'] == pk].fillna(0) ### Filter

    ###..Filter the Record as per Transact Date .............................
    dfB['ItemCost'] = dfB['itmCod'].map(SPList).fillna(0)
    dfB['EmpCost'] = dfB['itmCod'].map(empCostList).fillna(0)

    ###..Add a column 'ItemCost' and 'EmpCost' in QotAddi....................
    dfB = dfB[dfB['traDate'] == traDate]
    
    ###..Convert into List...................................................
    qotAddiItems = dfB.to_dict(orient="records") 


    context = {'lastOrder': pk, 'oBasic':qotBasi,  'addiOrder':qotAddiItems}
    return render(request, 'F1_Sales/sQotCotAdd.html', context)



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Order ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sOrderList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sOrderList.html', context)


def showOrderURL(request):
    #(Get All the Sales Order Detail)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    req_cols = ['id','soRef','soDat','cusName','qotRef', 'soTax', 'soTAT','spCName','opnClo','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    ### drop first row which is empty...
    df = df.drop(df.index[0])

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['soDat'] = pd.to_datetime(df['soDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Order and Deleted Record...
    df = df.drop_duplicates(subset=['soRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index).fillna('')


  ### Step 3. Read soStat.csv File -------------------------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['soRefSt'], keep='last')


  ### Step 4. Map soBasic.csv Open/Close with soStat.csv ---------------------
  ### ========================================================================
    opnClo_map = dict(zip(stat['soRefSt'], stat['opnCloSt']))
    df['opnClo'] = df['soRef'].map(opnClo_map).fillna(df['opnClo'])


  ### Step 5. Convert Data into Dictionary -----------------------------------
  ### ========================================================================
    Data = df.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 


def syncOrder(request): #URL to fetch data--

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File - to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfA.drop_duplicates(subset=['soRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic = dfBasic.sort_values('soRef') #sor by qotRef

    ### Save the data in qotBasic.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfBasic.to_csv(fPath, index=False)

    dfBasic['unique'] = dfBasic['soRef'].astype(str)+" "+dfBasic['traDate']


  ### Step 3. Read soAddi.csv File - to Load Data ----------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfB["unique"] = dfB['soRef'].astype(str)+" "+dfB['traDate']

    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    merged_df = pd.merge(dfB, dfBasic['unique'], on='unique', how='inner')
    ###---- Rearange Column to aboid any mistake
    merged_df = merged_df[['id','soRef','sno','itmCod','desc','qty','price','disc','tot','vat', 'traDate','action']]

    merged_df =merged_df.sort_values(['soRef','sno'], ascending = [True, True])

    ### Save the data in qotAddi.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
    merged_df.to_csv(fPath, index=False)


  ### Step 4 - Read soStat.csv File - to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape').fillna('')

    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    merged_stat = pd.merge(stat, dfBasic['traDate'], on='traDate', how='inner')
    merged_stat = merged_stat[['soRefSt','opnCloSt','traDate','action']]

    ### Save the data in qotStat.csv File...
    statPath =  "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    merged_stat.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sOrderAdd(request):
    #(to Show Sales Order Addition Page)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 1. Read soBasic.csv - to Get the last Sales Order Number ----------
  ### ========================================================================
    try: 
        req_cols = ['soRef', 'soDat']
        fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'soRef': [0]}
        df = pd.DataFrame(data)

    ## Get the last Order Number...
    lastOrder = df['soRef'].max()


    context = {'lastOrder': lastOrder }
    return render(request, 'F1_Sales/sOrderAdd.html', context)


def sQuotOpnList(request):
    #(Fetch All Open Quotation Detail not already converted into Sales Order Previously)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    req_cols = ["qotRef","qotDat", "cusCode", "cusName", "opnClo","action"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    df = df.drop(df.index[0]).fillna('') #drop first row which is dummy

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['qotDat'] = pd.to_datetime(df['qotDat']).dt.strftime('%Y-%m-%d')

    ###..Remove Duplicate Quote and Deleted Record...........................
    df = df.drop_duplicates(subset=['qotRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index)


  ### Step 3. Read qotStat.csv - file to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...   
    stat = stat.drop_duplicates(subset=['qotRefSt'], keep='last')  ##Drop Duplicate
    opnClo_map = dict(zip(stat['qotRefSt'], stat['opnCloSt'])) ## Map with stat opn/clo
    
    
  ### Step 4 - Map qotBasic.csv Open/Close with qotStat.csv ------------------
  ### ========================================================================
    df['opnClo'] = df['qotRef'].map(opnClo_map).fillna(df['opnClo']) ## Map with stat opn/clo
    df = df[df['opnClo'] != 'Closed']  ### remove 'Closed' Quote


  ### Step 5 - Read soBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    soPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    soDf = pd.read_csv(soPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate and Deleted Record...
    soDf = soDf.drop_duplicates(subset=['soRef'], keep='last')
    soDf = soDf.drop(soDf.loc[soDf['action']=='Deleted'].index).fillna('')

    #Select a column "qotRef" and convert into list to filter
    soList = soDf['qotRef'].tolist()

    #filter out all open sales Quote which is already converted into Sales Order
    filterData = df[~df['qotRef'].isin(soList)]


  ### Step 6 - Convert Data into Dictionary ----------------------------------
  ### ========================================================================
    Data = filterData.to_dict(orient="records")


    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def sQuotDetail(request, pk):
    #(Bring the Detail of Selected Quotation to create Sales Order)

    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Quote
    dfBasic = dfA[dfA['id'] == pk].fillna(0) ### Filter

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['qotDat'] = pd.to_datetime(dfBasic['qotDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['qotRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    ###..Get 'Transaction Date' Value..................................
    traDate = dfBasic.loc[dfBasic['qotRef'] == pk, 'traDate'].values[0]

    quotBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3. Read qotAddi.csv - file to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Quote
    dfB = dfB[dfB['qotRef'] == pk].fillna(0)

    ###..Filter the Record as per Transact Date .............................
    dfB = dfB[dfB['traDate'] == traDate]

    ###..Convert into List...................................................
    quotAddiItems = dfB.to_dict(orient="records") 


    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([quotBasi, quotAddiItems], safe=False) 


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sOrderAddUrl(request):
    #(to Save Quotation into Database)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Save Data in soBasic.csv file ----------------------------------
  ### ========================================================================
    basData = request.data[0]
    SoBasic =  {'id':basData['soRef'],         'soRef': basData['soRef'],
                'soDat':basData['soDat'],      'cusCode':basData['cusCode'],
                'cusName':basData['cusName'],  'soTBD':basData['soTBD'],
                'soTAD':basData['soTAD'],      'soTax': basData['soTax'],
                'soTAT':basData['soTAT'],      'shipTo':basData['shipTo'],
                'soComm':basData['soComm'],    'opnClo':"Open",
                'spCName':basData['spCName'],    'spCode':basData['spCode'],
                'qotRef':basData['qotRef'],    'qotDat':basData['qotDat'],
                'traDate':basData['traDate'],  'action':" ",
    }

    dfBasic = pd.DataFrame(SoBasic, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3. Save Data in soAddi.csv file -----------------------------------
  ### ========================================================================
    addiData = request.data[1]
    for data in addiData:
      Addi  = {'id': basData['soRef'],
                'soRef': basData['soRef'],
                'sno':data ['sno'],
                'itmCod':data ['itmcod'],
                'desc':data ['desc'],
                'qty':data ['qty'],
                'price':data ['price'],
                'disc':data ['disc'],
                'tot':data ['tot'],
                'vat':data ['vat'], 
                'traDate':basData['traDate'],
                'action':" " ,                             
        }
    
      dfAddi = pd.DataFrame(Addi, index=[0])
      fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
      dfAddi.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 4. Save Data in qotStat.csv file -----------------------------------
  ### ========================================================================
    QotStat =  {'qotRefSt':basData['qotRef'],
                'opnCloSt':"Closed",
                'traDate':basData['traDate'],
                'action':" ",
    }

    dfBasic = pd.DataFrame(QotStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 5. Save Data in soStat.csv file -----------------------------------
  ### ========================================================================
    basData = request.data[0]
    soStat =  {'soRefSt':basData['soRef'],
                'opnCloSt':"Open",
                'traDate':basData['traDate'],
                'action':" ",
    }

    SoStat = pd.DataFrame(soStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    SoStat.to_csv(fPath, index=False, header=False, mode='a')


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sOrderEdit(request, pk):
    #(to Show Quotation to edit)
    print(pk)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    pk = int(pk)
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['soRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['soDat'] = pd.to_datetime(dfBasic['soDat']).dt.strftime('%Y-%m-%d')
    dfBasic['qotDat'] = pd.to_datetime(dfBasic['qotDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['soRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in qotAddi
    List = dfBasic["traDate"] #.tolist()

    ### Convert Transaction Date to list to filter records in qotAddi
    soBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


    ### Step 3. Read soAddi.csv File -------------------------------------------
    ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfAddi = dfB[dfB['soRef'] == pk].fillna(0) ### Filter as per 'pk' selected quote
    filtered_df = dfAddi[dfAddi['traDate'].isin(List)] ### Filter by transaction Date

    ### Convert Transaction Date to list to filter records in qotAddi
    soAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary


    context = {'lastOrder': pk, 'oBasic':soBasi,  'addiOrder':soAddiItems}
    return render(request, 'F1_Sales/sOrderEdit.html', context)


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delSOrd(request, pk, Qot):
    pk = int(pk)
    Qot = int(Qot)
    print(pk)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


    ###--CHECK Delivery exist against such Order than don't Delete--------------
    #pk = 2300002
    req_cols = ["dlRef","soRef", "action"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')
    dfA = dfA.drop_duplicates(subset=['soRef'], keep='last') ### Remove Duplicate Record
    dfA = dfA.drop(dfA.loc[dfA['action']=='Deleted'].index)  ### Remove Deleted Record
    list = dfA['soRef'].tolist() ### Convert Column in LIst
    if pk in list: 
        return JsonResponse({'result': 'No'})

  ### Step 2. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['soRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['soRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['soRefSt'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['soRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['qotRefSt'] == Qot].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['qotRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['opnCloSt'] = 'Open' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Quotations/qotStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


    return Response('Items delete successfully!')



def sOrderPdf(request):
  #----------Get Data from html Page and convert into list---------------
    pk1 = request.GET.get('query_name')
    pk = int(pk1)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfBasic = dfA[dfA['soRef'] == pk].fillna(0) ### Filter

    ### Remove Duplicate Order and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['soRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in soAddi
    List = dfBasic["traDate"] #.tolist()

    soBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3. Read soAddi.csv File - to get Quotation Detail -----------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfAddi = dfB[dfB['soRef'] == pk].fillna(0) ### Filter Record as per 'pk' selected Order
    
    ### Filtere the 'Order' by Order "Target List"
    filtered_df = dfAddi[dfAddi['traDate'].isin(List)]
    soAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary

  ###--- If Want to see the Formation on Page before taking as pdf------
    #context = {"soBasi": soBasi, "soAddi":soAddiItems }
    #return render(request, 'F1_Sales/sOrderPdf.html', context)
  ###--- If Want to see the Formation on Page before taking as pdf------

    template_path = "../templates/F1_Sales/sOrderPdf.html"  #template to access
    context = {"soBasi": soBasi, "soAddi":soAddiItems }   # context is to pass data to html page before converting to PDF

    ###Create a Django response Object, and specify content_type as pdf
    ###---------------------------------------------------------------- 
    response = HttpResponse(content_type='application/pdf')  #normal django response
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'  #pdf to download - 'attachment' if comment out pdf will show on screen
    #response['Content-Disposition'] = 'filename="report.pdf"'  #pdf to download - 'attachment'

    ###Find the template and render it.(its a standard)..
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors')

    return response



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Delivery Notes ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sDeliveryList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sDeliveryList.html', context)


def showDeliveryURL(request):
    #(Get All the Sales Delivery Detail)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read dlBasic.csv File ------------------------------------------
  ### ========================================================================
    req_cols = ['id','dlRef','dlDat','cusName','soRef', 'dlTax', 'dlTAT','spCName','opnClo','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    ### drop first row which is empty...
    df = df.drop(df.index[0])

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['dlDat'] = pd.to_datetime(df['dlDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Delivery and Deleted Record...
    df = df.drop_duplicates(subset=['dlRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index).fillna('')


  ### Step 3. Read dlStat.csv File -------------------------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['dlRefSt'], keep='last')


  ### Step 4. Map dlBasic.csv Open/Close with dlStat.csv ---------------------
  ### ========================================================================
    opnClo_map = dict(zip(stat['dlRefSt'], stat['opnCloSt']))
    df['opnClo'] = df['dlRef'].map(opnClo_map).fillna(df['opnClo'])


  ### Step 5. Convert Data into Dictionary -----------------------------------
  ### ========================================================================
    Data = df.to_dict(orient="records")


    return JsonResponse(Data, safe=False) 


def syncDelivery(request): #URL to fetch data--

  ### Get Company and Year - to Load Data ------------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2. Read dlBasic.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfA.drop_duplicates(subset=['dlRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic = dfBasic.sort_values('dlRef') #sor by qotRef

    ### Save the data in qotBasic.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfBasic.to_csv(fPath, index=False)

    dfBasic['unique'] = dfBasic['dlRef'].astype(str)+" "+dfBasic['traDate']

  ### Step 3 - Read dlAddi.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfB["unique"] = dfB['dlRef'].astype(str)+" "+dfB['traDate']

    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    merged_df = pd.merge(dfB, dfBasic['unique'], on='unique', how='inner')
    ###---- Rearange Column to aboid any mistake
    merged_df = merged_df[['id','dlRef','sno','itmCod','desc','qty','price','disc','tot','vat','traDate','action']]

    merged_df =merged_df.sort_values(['dlRef','sno'], ascending = [True, True])

    ### Save the data in qotAddi.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    merged_df.to_csv(fPath, index=False)


  ### Step 4 - Read dlStat.csv File - to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    stat = stat.drop_duplicates(subset=['dlRefSt'], keep='last')
    stat = stat.drop(stat.loc[stat['action']=='Deleted'].index)

    ### Save the data in qotStat.csv File...
    statPath =  "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    stat.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sDeliveryAdd(request):
    #(to Show Sales Order Addition Page)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 1. Read dlBasic.csv - to Get the last Delivery Number -------------
  ### ========================================================================
    try: 
        req_cols = ['dlRef', 'dlDat']
        fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'dlRef': [0]}
        df = pd.DataFrame(data)

    ## Get the last Delivery Number...
    lastDelivery = df['dlRef'].max()


    context = {'lastDelivery': lastDelivery }
    return render(request, 'F1_Sales/sDeliveryAdd.html', context)


def sOrderOpnList(request):  #Get the list of all Open Sales Order only .........

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Read qotBasic.csv - file to Load Data ----------------------------------
  ### ========================================================================
    req_cols = ["soRef","soDat", "cusCode", "cusName", "opnClo","action"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    df = df.drop(df.index[0]).fillna('') #drop first row which is dummy

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['soDat'] = pd.to_datetime(df['soDat']).dt.strftime('%Y-%m-%d')

    ## Remove Duplicate Order and Deleted Record...
    df = df.drop_duplicates(subset=['soRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Delete'].index)


  ### Step 3 - Read soStat.csv - file to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')
    
    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['soRefSt'], keep='last')
    

  ### Map soBasic.csv Open/Close with soStat.csv ----------------------------
  ### =======================================================================
    opnClo_map = dict(zip(stat['soRefSt'], stat['opnCloSt']))   ##map with stat
    df['opnClo'] = df['soRef'].map(opnClo_map).fillna(df['opnClo'])


  ### Step 5 - Read dlBasic.csv - file to Load Data -------------------------
  ### =======================================================================
    dlPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dlDf = pd.read_csv(dlPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate and Deleted Record...
    dlDf = dlDf.drop_duplicates(subset=['dlRef'], keep='last')
    dlDf = dlDf.drop(dlDf.loc[dlDf['action']=='Deleted'].index).fillna('')

    #Select a column "qotRef" and convert into list to filter
    dlList = dlDf['soRef'].tolist() 

    #filter out all open sales Quote which is already converted into Sales Order
    filterData = df[~df['soRef'].isin(dlList)]


  ### 6 - Convert Data into Dictionary --------------------------------------
  ### =======================================================================

    ### Convert Data into Json Dictionary
    Data = filterData.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def sOrderDetail(request, pk):  #Fetch Sales Order Detail for initially load .....
    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read qotBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Order
    dfBasic = dfA[dfA['soRef'] == pk].fillna(0) 

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['soDat'] = pd.to_datetime(dfBasic['soDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Order and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['soRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ###..Get 'Transaction Date' Value..................................
    traDate = dfBasic.loc[dfBasic['soRef'] == pk, 'traDate'].values[0]

    soBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 2. Read soAddi.csv - file to Load Data ----------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Quote
    dfB = dfB[dfB['soRef'] == pk].fillna(0)

    ###..Filter the Record as per Transact Date .............................
    dfB = dfB[dfB['traDate'] == traDate].fillna('')

    ###..Convert into List...................................................
    soAddiItems = dfB.to_dict(orient="records") 

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([soBasi, soAddiItems], safe=False) 


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sDeliveryAddURL(request):
    #(to Save Quotation into Database)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Save Data in dlBasic.csv file ---------------------------------
  ### ========================================================================
    basData = request.data[0]   
    DlBasic =  {'id':basData['dlRef'],         'dlRef': basData['dlRef'],
                'dlDat':basData['dlDat'],      'cusCode':basData['cusCode'],
                'cusName':basData['cusName'],  'dlTBD':basData['dlTBD'],
                'dlTAD':basData['dlTAD'],      'dlTax': basData['dlTax'],
                'dlTAT':basData['dlTAT'],      'shipTo':basData['shipTo'],
                'dlComm':basData['dlComm'],    'opnClo':"Open",
                'spCName':basData['spCName'],    'spCode':basData['spCode'],
                'soRef':basData['soRef'],    'soDat':basData['soDat'],
                'traDate':basData['traDate'],  'action':" ",
    }
 
    dfBasic = pd.DataFrame(DlBasic, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3 - Save Data in soStat.csv file ----------------------------------
  ### ========================================================================
    addiData = request.data[1]
    addRecords = []
    for data in addiData:
      Addi  = {'id': basData['dlRef'],
                'dlRef': basData['dlRef'],
                'sno':data ['sno'],
                'itmCod':data ['itmcod'],
                'desc':data ['desc'],
                'qty':data ['qty'],
                'price':data ['price'],
                'disc':data ['disc'],
                'tot':data ['tot'],
                'vat':data ['vat'],
                'traDate':basData['traDate'],
                'action':" " ,                             
        }
      addRecords.append(Addi)  # Add the dictionary to the list

    dfAddi = pd.DataFrame(addRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dfAddi.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 4 - Save Data in soStat.csv file ----------------------------------
  ### ========================================================================
    soStat =  {'soRef': basData['soRef'],
                'opnCloSt':"Closed",
                'traDate':basData['traDate'],
                'action':" ",
    }
    
    dfBasic = pd.DataFrame(soStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 5 - Save Data in dlStat.csv file ----------------------------------
  ### ========================================================================
    dlStat =  {'dlRef': basData['dlRef'],
                'opnCloSt':"Open",
                'traDate':basData['traDate'],
                'action':" ",
    }
    
    DlBasic = pd.DataFrame(dlStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    DlBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 6 - Save Data in ItemMovement.csv file ----------------------------------
  ### ========================================================================
    itmRecords = []
    COGS = 0
    for data in addiData:
      COGS = COGS + int(data['wac']) ### Sum Total Value of Cost of Sales
      Qty = int(data['qty']) * -1
      itemMov =  {'id':basData['dlRef'],        'itmCode':data ['itmcod'],
                  'itmName':data ['desc'],      'traDat':basData['dlDat'],
                  'qtyPU':0,                    'costPU':0,
                  'qtyTOT':Qty,        'desc':'Sales of Product', 
                  'Remarks':"Sales",
                  'traDate':basData['traDate'], 'action':" " ,  
                  }
      itmRecords.append(itemMov)  # Add the dictionary to the list

    itemDf = pd.DataFrame(itmRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/itemMovement.csv"
    itemDf.to_csv(fPath, index=False, header=False, mode='a')




  ### Step 7 - Journal Entry Entries.csv file --------------------------------
  ### ========================================================================
    addRecords = []
    Inventory = COGS * -1

    cogs =  {'Ref':basData['dlRef'], 'type': 'dl', 'Date':basData['dlDat'], 'accCode':60110001, 'accName':'Cogs1','amount':COGS , 'Comm':basData['dlComm'] ,'traDate':basData['traDate'], 'action':" "}
    sales =  {'Ref':basData['dlRef'], 'type': 'dl', 'Date':basData['dlDat'], 'accCode':37000001, 'accName':'Inventory at Cost','amount':Inventory, 'Comm':basData['dlComm'],'traDate':basData['traDate'], 'action':" "}
    addRecords.append(cogs)
    addRecords.append(sales)

    Journal = pd.DataFrame(addRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    Journal.to_csv(fPath, index=False, header=False, mode='a')



    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sDeliveryEdit(request, pk):
    #(to Show Quotation to edit)
    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['dlRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['dlDat'] = pd.to_datetime(dfBasic['dlDat']).dt.strftime('%Y-%m-%d')
    dfBasic['soDat'] = pd.to_datetime(dfBasic['soDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['dlRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in qotAddi
    List = dfBasic["traDate"] #.tolist()

    ### Convert Transaction Date to list to filter records in qotAddi
    dlBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 2. Read soAddi.csv File -------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfAddi = dfB[dfB['dlRef'] == pk].fillna(0) ### Filter as per 'pk' selected quote

    filtered_df = dfAddi[dfAddi['traDate'].isin(List)] ### Filter by transaction Date

    ### Convert Transaction Date to list to filter records in qotAddi
    dlAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary

    context = {'lastOrder': pk, 'dlBasic':dlBasi,  'dlAddiItems':dlAddiItems}
    return render(request, 'F1_Sales/sDeliveryEdit.html', context)


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delDelivery(request, pk, Ord):
    pk = int(pk)
    Ord = int(Ord)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read soBasic.csv File -----------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['dlRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote
 
    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['dlRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3 - Read dlState.csv File -----------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['dlRefSt'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['dlRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 4 - Read soStat.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['soRefSt'] == Ord].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['soRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['opnCloSt'] = 'Open' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 5 - Read ItemMovement.csv File ------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/itemMovement.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['id'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['itmCode'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/itemMovement.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 6 - Read Journals.csv File ----------------------------------------
  ### ========================================================================
    #pk= 2300002
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfA['unique'] = dfA['Ref'].astype(str)+ '-' +dfA['Type']
    itemPk = str(pk)+'-dl'
    dfStat = dfA[dfA['unique'] == itemPk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['accCode'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted
    dfStat = dfStat.drop('unique', axis=1)

    ### Save the record(dataframe) in csv file
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')

    return Response('Items delete successfully!')


def sDeliveryPdf(request):
  #----------Get Data from html Page and convert into list---------------
    pk1 = request.GET.get('query_name')
    pk = int(pk1)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read soBasic.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfBasic = dfA[dfA['dlRef'] == pk].fillna(0) ### Filter

    ### Remove Duplicate Order and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['dlRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in soAddi
    List = dfBasic["traDate"] #.tolist()

    dlBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3. Read soAddi.csv File - to get Quotation Detail -----------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfAddi = dfB[dfB['dlRef'] == pk].fillna(0) ### Filter Record as per 'pk' selected Order    
    
    ### Filtere the 'Order' by Order "Target List"
    filtered_df = dfAddi[dfAddi['traDate'].isin(List)]
    dlAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary

  ###--- If Want to see the Formation on Page before taking as pdf------
    #context = {"soBasi": soBasi, "soAddi":soAddiItems }
    #return render(request, 'F1_Sales/sDeliveryPdf.html', context)
  ###--- If Want to see the Formation on Page before taking as pdf------

    template_path = "../templates/F1_Sales/sDeliveryPdf.html"  #template to access
    context = {"dlBasi": dlBasi, "dlAddi":dlAddiItems }   # context is to pass data to html page before converting to PDF

    ###Create a Django response Object, and specify content_type as pdf
    ###---------------------------------------------------------------- 
    response = HttpResponse(content_type='application/pdf')  #normal django response
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'  #pdf to download - 'attachment' if comment out pdf will show on screen
    #response['Content-Disposition'] = 'filename="report.pdf"'  #pdf to download - 'attachment'

    ###Find the template and render it.(its a standard)..
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors')

    return response




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Invoices ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sInvoiceList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sInvoiceList.html', context)


def showInvoiceURL(request):
    #(Get Sales Order Detail from DataBase)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read dlBasic.csv File -----------------------------------------
  ### ========================================================================
    req_cols = ['id','siRef','siDat','cusName','dlRef', 'siTax', 'siTAT','spCName','opnClo','action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    ### drop first row which is empty...
    df = df.drop(df.index[0])

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['siDat'] = pd.to_datetime(df['siDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Delivery and Deleted Record...
    df = df.drop_duplicates(subset=['siRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index).fillna('')


  ### Step 3 - Read siStat.csv File ------------------------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['siRefSt'], keep='last')


  ### Step 4 - Map dlBasic.csv Open/Close with dlStat.csv --------------------
  ### ========================================================================
    opnClo_map = dict(zip(stat['siRefSt'], stat['opnCloSt']))
    df['opnClo'] = df['siRef'].map(opnClo_map).fillna(df['opnClo'])

    ### Convert Data into Json Dictionary
    Data = df.to_dict(orient="records")


    return JsonResponse(Data, safe=False) 


def syncInvoice(request): #URL to fetch data--

  ### Get Company and Year - to Load Data ------------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read siBasic.csv File - to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfA.drop_duplicates(subset=['siRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic = dfBasic.sort_values('siRef') #sor by qotRef

    ### Save the data in qotBasic.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfBasic.to_csv(fPath, index=False)

    dfBasic['unique'] = dfBasic['siRef'].astype(str)+" "+dfBasic['traDate']

  ### Step 3 - Read siAddi.csv File - to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfB["unique"] = dfB['siRef'].astype(str)+" "+dfB['traDate']

    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    merged_df = pd.merge(dfB, dfBasic['unique'], on='unique', how='inner')
    ###---- Rearange Column to aboid any mistake
    merged_df = merged_df[['id','siRef','sno','itmCod','desc','qty','price','disc','tot','vat','traDate','action']]

    merged_df =merged_df.sort_values(['siRef','sno'], ascending = [True, True])

    ### Save the data in qotAddi.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siAddi.csv"
    merged_df.to_csv(fPath, index=False)


  ### Step 4 - Read siStat.csv File - to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate Quote and Deleted Record...
    stat = stat.drop_duplicates(subset=['siRefSt'], keep='last')
    stat = stat.drop(stat.loc[stat['action']=='Deleted'].index)

    ### Save the data in qotStat.csv File...
    statPath =  "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    stat.to_csv(statPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sInvoiceAdd(request):
    #(to Show Sales Order Addition Page)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read siBasic.csv - to Get the last Invoice Number -------------
  ### ========================================================================
    try: 
        req_cols = ['siRef', 'siDat']
        fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'siRef': [0]}
        df = pd.DataFrame(data)

    ## Get the last Order Number...
    lastInvoice = df['siRef'].max()


    context = {'lastInvoice': lastInvoice }
    return render(request, 'F1_Sales/sInvoiceAdd.html', context)


def sDeliveryOpnList(request):  #Get the list of all Open Sales Order only .........

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])

    
  ### Step 2 - Read dlBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    req_cols = ["dlRef","dlDat", "cusCode", "cusName", "opnClo","action"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    df = df.drop(df.index[0]).fillna('') #drop first row which is dummy

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['dlDat'] = pd.to_datetime(df['dlDat']).dt.strftime('%Y-%m-%d')

    ## Remove Duplicate Order and Deleted Record...
    df = df.drop_duplicates(subset=['dlRef'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index)


  ### Step 3 - Read dlStat.csv - file to Load Data ---------------------------
  ### ========================================================================
    statPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    stat = pd.read_csv(statPath, index_col=False, encoding='unicode_escape')

    ### Remove Duplicate and Deleted Record...
    stat = stat.drop_duplicates(subset=['dlRefSt'], keep='last')

    
  ### Step 4 - Map dlBasic.csv Open/Close with dlStat.csv --------------------
  ### ========================================================================
    opnClo_map = dict(zip(stat['dlRefSt'], stat['opnCloSt']))   ##map with stat
    df['opnClo'] = df['dlRef'].map(opnClo_map).fillna(df['opnClo'])

    
  ### Step 5 - Read siBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    dlPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    siDf = pd.read_csv(dlPath, index_col=False, encoding='unicode_escape').fillna('')

    ### Remove Duplicate and Deleted Record...
    siDf = siDf.drop_duplicates(subset=['siRef'], keep='last')
    siDf = siDf.drop(siDf.loc[siDf['action']=='Deleted'].index).fillna('')

    #Select a column "dlRef" and convert into list to filter
    siList = siDf['dlRef'].tolist() 

    #filter out all open sales Quote which is already converted into Sales Order
    filterData = df[~df['dlRef'].isin(siList)]

    
  ### Step 6 - Convert Data into Dictionary ----------------------------------
  ### ========================================================================
    Data = filterData.to_dict(orient="records")


    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def sDeliveryDetail(request, pk):  #Fetch Sales Order Detail for initially load .....
    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read soBasic.csv - file to Load Data --------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Order
    dfBasic = dfA[dfA['dlRef'] == pk].fillna(0) 

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['dlDat'] = pd.to_datetime(dfBasic['dlDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Order and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['dlRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    ###..Get 'Transaction Date' Value..................................
    traDate = dfBasic.loc[dfBasic['dlRef'] == pk, 'traDate'].values[0]

    dlBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


    
  ### Get Cutomer Detail - To Get Credit Term and other details --------------
  ### ========================================================================
    ###..Get 'Get Customer Code' Value..................................
    custCode = dfBasic.loc[dfBasic['dlRef'] == pk, 'cusCode'].values[0]
    
    ### Read "CustMaster.csv" file
    req_cols = ["cusCode","cusCrLim", "cusPytTerm", "cusLegName", "cusTRN"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Customers/CustMaster.csv"
    dfC = pd.read_csv(fPath, index_col=False, usecols=req_cols, encoding='unicode_escape')

    ### Filter data based on 'Customer Code' selected Order
    dfCustomer = dfC[dfC['cusCode'] == custCode].fillna(0) 
    ###..Convert into List...................................................
    cusDetail = dfCustomer.to_dict(orient="records") 


  ### Step 3 - Read soAddi.csv - file to Load Data ---------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter data based on 'pk' selected Quote
    dfB = dfB[dfB['dlRef'] == pk].fillna(0)

    ###..Filter the Record as per Transact Date .............................
    dfB = dfB[dfB['traDate'] == traDate].fillna('')

    ###..Convert into List...................................................
    dlAddiItems = dfB.to_dict(orient="records") 


    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([dlBasi, dlAddiItems, cusDetail], safe=False) 


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sInvoiceAddURL(request):
    #(to Save Quotation into Database)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])



  ### Step 2 - Save Data in siBasic.csv file ---------------------------------
  ### ========================================================================
    basData = request.data[0]  
    SiBasic={'id':basData['siRef'],        'siRef':basData['siRef'], 
             'siDat':basData['siDat'],     'cusCode':basData['cusCode'], 
             'cusName':basData['cusName'],   'siTBD':basData['siTBD'], 
             'siTAD':basData['siTAD'],     'siTax':basData['siTax'], 
             'siTAT':basData['siTAT'],     'shipTo':basData['shipTo'],
             'siComm':basData['siComm'],    'opnClo':'Open', 
             'spCName':basData['spCName'],    'spCode':basData['spCode'],
             'dlRef':basData['dlRef'],     'dlDat':basData['dlDat'],
             'traDate':basData['traDate'],   'action':basData['action'],
            }

    dfBasic = pd.DataFrame(SiBasic, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3 - Save Data in soAddi.csv file ----------------------------------
  ### ========================================================================
    addiData = request.data[1]
    addRecords = []
    for data in addiData:
      Addi  = { 'id': basData['siRef'],      'dlRef': basData['siRef'],
                'sno':data ['sno'],          'itmCod':data ['itmcode'],
                'desc':data ['desc'],        'qty':data ['qty'],
                'price':data ['price'],      'disc':data ['disc'],
                'tot':data ['tot'],          'vat':data['vat'],
                'traDate':basData['traDate'],'action':basData['action'],                             
        }
    
      addRecords.append(Addi)  # Add the dictionary to the list

    dfAddi = pd.DataFrame(addRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siAddi.csv"
    dfAddi.to_csv(fPath, index=False, header=False, mode='a')



  ### Step 4 - Save Data in siStat.csv file ----------------------------------
  ### ========================================================================
    siStat =  {'siRefSt':basData['siRef'], 'opnCloSt':"Open",
               'traDate':basData['traDate'],   'action':basData['action']}

    SiStat = pd.DataFrame(siStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    SiStat.to_csv(fPath, index=False, header=False, mode='a')



  ### Step 5 - Save Data in dlStat.csv file ----------------------------------
  ### ========================================================================
    dlStat =  {'dlRefSt':basData['dlRef'], 'opnCloSt':"Closed",
               'traDate':basData['traDate'],   'action':basData['action']}

    dfBasic = pd.DataFrame(dlStat, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 6 - Save Data in Customers.csv file -------------------------------
  ### ========================================================================
    customers =  {'Ref':basData['siRef'],     'type': 'si', 'siDat':basData['siDat'], 
                  'cusCode':basData['cusCode'], 'cusName':basData['cusName'],
                  'siTAT':basData['siTAT'],     'siComm':basData['siComm'],
                  'ptStat':'Outstanding',       'dueDate':basData['crPeiod'],
                  'traDate':basData['traDate'],   'action':basData['action'],
            }
    
    custDf = pd.DataFrame(customers, index=[0])
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Customers/Customers.csv"
    custDf.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 7 - Journal Entry Entries.csv file --------------------------------
  ### ========================================================================
    addRecords = []
    VAT = (basData['siTax'])*-1
    SALES = (basData['siTAD'])*-1

    customer =  {'Ref':basData['siRef'], 'type': 'si', 'Date':basData['siDat'], 'accCode':basData['cusCode'], 'accName':basData['cusName'], 'amount':basData['siTAT'] ,'Comm':basData['siComm'],'traDate':basData['traDate'], 'action':basData['action']}
    vat =  {'Ref':basData['siRef'], 'type': 'si', 'Date':basData['siDat'], 'accCode':44280001, 'accName':'VAT Output Tax Payable', 'amount':VAT,'Comm':basData['siComm'],'traDate':basData['traDate'], 'action':basData['action']}
    sales =  {'Ref':basData['siRef'], 'type': 'si', 'accCode':70120001, 'Date':basData['siDat'], 'accName':'Credit Sales', 'Comm':basData['siComm'],'amount':SALES,'traDate':basData['traDate'], 'action':basData['action']}
    addRecords.append(customer)
    addRecords.append(vat)
    addRecords.append(sales)

    Journal = pd.DataFrame(addRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    Journal.to_csv(fPath, index=False, header=False, mode='a')


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sInvoiceEdit(request, pk):
    pk = int(pk)
    #(to Show Quotation to edit)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read siBasic.csv File -----------------------------------------
  ### ========================================================================
    #pk = 2300001
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['siRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### file doesn't recongnize date formate first convert into date and than strftime
    dfBasic['siDat'] = pd.to_datetime(dfBasic['siDat']).dt.strftime('%Y-%m-%d')
    dfBasic['dlDat'] = pd.to_datetime(dfBasic['dlDat']).dt.strftime('%Y-%m-%d')

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['siRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Delete'].index)

    ### Convert Transaction Date to list to filter records in qotAddi
    List = dfBasic["traDate"] #.tolist()

    ### Convert Transaction Date to list to filter records in qotAddi
    siBasi = dfBasic.to_dict(orient="records") ### convert into dictionary


  ### Step 3 - Read siAddi.csv File ------------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfAddi = dfB[dfB['siRef'] == pk].fillna(0) ### Filter as per 'pk' selected quote

    filtered_df = dfAddi[dfAddi['traDate'].isin(List)] ### Filter by transaction Date

    ### Convert Transaction Date to list to filter records in qotAddi
    siAddiItems = filtered_df.to_dict(orient="records") ### convert into dictionary


  ### Get Cutomer Detail - To Get Credit Term and other details --------------
  ### ========================================================================
    ###..Get 'Get Customer Code' Value..................................
    custCode = dfBasic.loc[dfBasic['siRef'] == pk, 'cusCode'].values[0]

    ### Read "CustMaster.csv" file
    req_cols = ["cusCode","cusCrLim", "cusPytTerm", "cusLegName", "cusTRN"]
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Customers/CustMaster.csv"
    dfC = pd.read_csv(fPath, index_col=False, usecols=req_cols, encoding='unicode_escape')

    ### Filter data based on 'Customer Code' selected Order
    dfCustomer = dfC[dfC['cusCode'] == custCode].fillna(0) 
    ###..Convert into List...................................................
    cusDetail = dfCustomer.to_dict(orient="records") 

    context = {'lastOrder': pk, 'siBasic':siBasi,  'siAddiItems':siAddiItems, 'cusDetail':cusDetail}
    return render(request, 'F1_Sales/sInvoiceEdit.html', context)


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delInvoice(request, pk, dl):
    pk = int(pk)
    dl = int(dl)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read siBasic.csv File -----------------------------------------
  ### ========================================================================
    #pk = 2300001
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfBasic = dfA[dfA['siRef'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfBasic = dfBasic.drop_duplicates(subset=['siRef'], keep='last')
    dfBasic = dfBasic.drop(dfBasic.loc[dfBasic['action']=='Deleted'].index)

    dfBasic['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 3 - Read siState.csv File -----------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['siRefSt'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['siRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 4 - Read dlStat.csv File ------------------------------------------
  ### ========================================================================
    #dl= 2300004
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['dlRefSt'] == dl].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['dlRefSt'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['opnCloSt'] = 'Open' ### in 'action' column add the word 'Deleted'   

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 5 - Read Customers.csv File ---------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Customers/Customers.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')
    dfStat = dfA[dfA['Ref'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['Ref'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted'

    ### Save the record(dataframe) in csv file
    fPath = fPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Customers/Customers.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


  ### Step 6 - Read Journals.csv File ----------------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    dfA['unique'] = dfA['Ref'].astype(str)+ '-' +dfA['Type']
    itemPk = str(pk)+'-si'
    dfStat = dfA[dfA['unique'] == itemPk].fillna(0) ### Filter data as per 'pk' selected quote

    ### Remove Duplicate Quote and Deleted Record...
    dfStat = dfStat.drop_duplicates(subset=['accCode'], keep='last')
    dfStat = dfStat.drop(dfStat.loc[dfStat['action']=='Deleted'].index)

    dfStat['action'] = 'Deleted' ### in 'action' column add the word 'Deleted
    dfStat = dfStat.drop('unique', axis=1)

    ### Save the record(dataframe) in csv file
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    dfStat.to_csv(fPath, index=False, header=False, mode='a')


    return Response('Items delete successfully!')




#☰☰☰ Invoice Drill Down ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def tInvoiceDD(request, pk):
    sInv = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### 2. Reading of invoices.CSV file ----------------------------------------
  ### ========================================================================
    req_cols = ["siRef", "siDat", "cusName", "siTAT", "dlRef", "dlDat", "action"]
    siPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    siDf = pd.read_csv(siPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    siStatPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siStat.csv"
    siStatDf = pd.read_csv(siStatPath, index_col=False, encoding='unicode_escape')

    ### Filter data by Sales Invoice Number ---------------------------------------
    #sInv = 2300131
    siDf = siDf[siDf['siRef'] == sInv].fillna(0) 
    siStatDf = siStatDf[siStatDf['siRefSt'] == sInv].fillna(0) 

    ### Remove Duplicate Sales Invoice and Deleted Record...
    siDf = siDf.drop_duplicates(subset=['siRef'], keep='last')
    siDf = siDf.drop(siDf.loc[siDf['action']=='Deleted'].index).fillna('')

    ### Remove Duplicate Sales Invoice and Deleted Record...
    siStatDf = siStatDf.drop_duplicates(subset=['siRefSt'], keep='last')
    siStatDf = siStatDf.drop(siStatDf.loc[siStatDf['action']=='Deleted'].index).fillna('')
    siStatDf = siStatDf.rename(columns={"siRefSt": "siRef"})
    siMerge = pd.merge(siDf, siStatDf, on="siRef")

    ###..Get 'Quotation number' Value..................................
    dlNm = siDf.loc[siDf['siRef'] == sInv, 'dlRef'].values[0]

    ###-- Record --###
    siData = siMerge.to_dict(orient="records") ### convert into dictionary

  ### 3. Reading of deliveries.CSV file --------------------------------------
  ### ========================================================================
    req_cols = ["dlRef", "dlDat", "cusName", "dlTAT", "soRef", "soDat", "traDate", "action"]
    dlPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dlDf = pd.read_csv(dlPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    dlStatPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlStat.csv"
    dlStatDf = pd.read_csv(dlStatPath, index_col=False, encoding='unicode_escape')

    ### Filter data by Delivery Note Number ---------------------------------------
    dlDf = dlDf[dlDf['dlRef'] == dlNm].fillna(0) 
    dlStatDf = dlStatDf[dlStatDf['dlRefSt'] == dlNm].fillna(0) 

    ### Remove Duplicate Delivery Note and Deleted Record...
    dlDf = dlDf.drop_duplicates(subset=['dlRef'], keep='last')
    dlDf = dlDf.drop(dlDf.loc[dlDf['action']=='Deleted'].index).fillna('')

    ### Remove Duplicate Sales Invoice and Deleted Record...
    dlStatDf = dlStatDf.drop_duplicates(subset=['dlRefSt'], keep='last')
    dlStatDf = dlStatDf.drop(dlStatDf.loc[dlStatDf['action']=='Deleted'].index).fillna('')
    dlStatDf = dlStatDf.rename(columns={"dlRefSt": "dlRef"})
    dlMerge = pd.merge(dlDf, dlStatDf, on="dlRef")

    ###-- Record --###
    dlData = dlMerge.to_dict(orient="records") ### convert into dictionary

    ###..Get 'Quotation number' Value..................................
    soNm = dlDf.loc[dlDf['dlRef'] == dlNm, 'soRef'].values[0]


  ### 4. Reading of Orders.CSV file ------------------------------------------
  ### ========================================================================
    req_cols = ["soRef", "soDat", "cusName", "soTAT", "qotRef", "qotDat", "action"]
    soPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soBasic.csv"
    soDf = pd.read_csv(soPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    soStatPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Orders/soStat.csv"
    soStatDf = pd.read_csv(soStatPath, index_col=False, encoding='unicode_escape')

    ### Filter data by Sales Order Number ---------------------------------------
    soDf = soDf[soDf['soRef'] == soNm].fillna(0) 
    soStatDf = soStatDf[soStatDf['soRefSt'] == soNm].fillna(0) 

    ### Remove Duplicate Sales Order and Deleted Record...
    soDf = soDf.drop_duplicates(subset=['soRef'], keep='last')
    soDf = soDf.drop(soDf.loc[soDf['action']=='Deleted'].index).fillna('')

    ### Remove Duplicate Sales Invoice and Deleted Record...
    soStatDf = soStatDf.drop_duplicates(subset=['soRefSt'], keep='last')
    soStatDf = soStatDf.drop(soStatDf.loc[soStatDf['action']=='Deleted'].index).fillna('')
    soStatDf = soStatDf.rename(columns={"soRefSt": "soRef"})
    soMerge = pd.merge(soDf, soStatDf, on="soRef")

    ###-- Record --###
    soData = soMerge.to_dict(orient="records") ### convert into dictionary

    ###..Get 'Quotation number' Value..................................
    qotNm = soDf.loc[soDf['soRef'] == soNm, 'qotRef'].values[0]

  ### 4. Reading of Orders.CSV file ------------------------------------------
  ### ========================================================================
    req_cols = ["qotRef", "qotDat", "cusName", "qotTAT", "action"]
    qotPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/quotations/qotBasic.csv"
    qotDf = pd.read_csv(qotPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    qotStatPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/quotations/qotStat.csv"
    qotStatDf = pd.read_csv(qotStatPath, index_col=False, encoding='unicode_escape')

    ### Filter data by Sales Order Number ---------------------------------------
    qotDf = qotDf[qotDf['qotRef'] == qotNm].fillna(0) 
    qotStatDf = qotStatDf[qotStatDf['qotRefSt'] == qotNm].fillna(0) 

    ### Remove Duplicate Sales Order and Deleted Record...
    qotDf = qotDf.drop_duplicates(subset=['qotRef'], keep='last')
    qotDf = qotDf.drop(qotDf.loc[qotDf['action']=='Deleted'].index).fillna('')

    ### Remove Duplicate Sales Invoice and Deleted Record...
    qotStatDf = qotStatDf.drop_duplicates(subset=['qotRefSt'], keep='last')
    qotStatDf = qotStatDf.drop(qotStatDf.loc[qotStatDf['action']=='Deleted'].index).fillna('')
    qotStatDf = qotStatDf.rename(columns={"qotRefSt": "qotRef"})
    qotMerge = pd.merge(qotDf, qotStatDf, on="qotRef")

    ###-- Record --###
    qotData = qotMerge.to_dict(orient="records") ### convert into dictionary


    #records = [siData, dlData, soData, qotData]    
    #context = {'records':records}

    context = {'siData':siData, 'dlData':dlData, 'soData':soData, 'qotData':qotData }
    return render(request, 'F1_Sales/tInvoiceDD.html', context)




#☰☰☰ SALES ANALYSIS ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def f1_SalesAnalysis(request):

  ### Step 1 - Loading of Excel Data in Pandas Based on Region and Type------
  ### =======================================================================

   ## 1a. Define Year, Month, Type, Region, Segment and Currency
   ## .......................................................................
    cYear = "2021"
    pYear = int(cYear)-1; pYear = str(pYear)
    selMonth = "23"
    Type = "-1st-"
    selRegion = "GCC" #"Group" #"GCC"
    selSegment = "1"
    selCurrency = "AED"


   ## 1b. Select Columns to load Data
   ## .......................................................................
    req_cols = ['1a.Revenue', '2a.Cost of Sales', 'Month', 'Region', 'Country', 'Department']


   ## 1c. Read CSV files based on Selected Region and Year
   ## .......................................................................
    if( selRegion == "Group"):
        CYearGCC = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/tempGCC.csv")
        CYearLevant = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/tempLevant.csv")
        CYearMCS = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/tempMCS.csv")
        framesCY = (CYearGCC , CYearLevant, CYearMCS)

        CYear  = pd.concat(framesCY)
        CYear.reset_index(inplace=True)
        CYear.drop(CYear[CYear['Type'] == "IC" ].index, inplace = True)

        PYearGCC = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/tempGCC.csv")
        PYearLevant = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/tempLevant.csv")
        PYearMCS = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/tempMCS.csv")
        framesPY = (PYearGCC , PYearLevant, PYearMCS)

        PYear  = pd.concat(framesPY)
        PYear.reset_index(inplace=True)
        PYear.drop(PYear[PYear['Type'] == "IC" ].index, inplace = True)

        BYearGCC = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/GCC-combineBdg"+Type+".csv", usecols=req_cols)
        BYearLevant = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/Levant-combineBdg"+Type+".csv", usecols=req_cols)
        BYearAfrica = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/Africa-combineBdg"+Type+".csv", usecols=req_cols)
        BYearCD = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/CD-combineBdg"+Type+".csv", usecols=req_cols)
        BYearMCS = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/MCS-combineBdg"+Type+".csv", usecols=req_cols)
        framesBY = (BYearGCC , BYearLevant, BYearAfrica, BYearCD, BYearMCS)
        BYear  = pd.concat(framesBY)
        BYear.reset_index(inplace=True)

    elif( selRegion == "GCC"):
        #CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/"+selRegion+".csv")
        CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/GCC.csv")
        PYear = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/GCC.csv")
        BYear_GCC = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/"+selRegion+"-combineBdg"+Type+".csv", usecols=req_cols)
        BYear_GCCCD = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/CD-combineBdg"+Type+".csv", usecols=req_cols)
        frames = (BYear_GCC , BYear_GCCCD)
        BYear  = pd.concat(frames)
        BYear.reset_index(inplace=True)

    elif( selRegion == "MCS"):
        #CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/"+selRegion+".csv")
        CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/tempMCS.csv")
        PYear = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/tempMCS.csv")
        BYear = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/"+selRegion+"-combineBdg"+Type+".csv", usecols=req_cols)
        CYear.reset_index(inplace=True)
        selRegion = "MCS"

    elif( selRegion == "Levant"):
        #CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/"+selRegion+".csv")
        CYear = pd.read_csv("Data/4_Sales/"+cYear+"/salSummary/tempLevant.csv")
        PYear = pd.read_csv("Data/4_Sales/"+pYear+"/salSummary/tempLevant.csv")
        BYear = pd.read_csv("Data/1_Budget/"+cYear+"/Yearly/"+selRegion+"-combineBdg"+Type+".csv", usecols=req_cols)
        CYear.reset_index(inplace=True)
        selRegion = "Levant"

    else:
        pass


   ## 1d. Rename the selected Columns as per requirement
   ## .......................................................................
    PYear.rename(columns = {'CY_CoS':'PY_CoS', 'CY_Revenue':'PY_Revenue'}, inplace=True)



  ### Step 2 - Select Segment -----------------------------------------------
  ### =======================================================================
    selSegment = "1"
    if( selSegment == '1'):
            CYear = CYear
            sSegment = "Standard"
    elif( selSegment == '2'):
            CYear.drop(CYear[CYear['Type'] == "CD" ].index, inplace = True)
            PYear.drop(PYear[PYear['Type'] == "CD" ].index, inplace = True)
            BYear.drop(BYear[BYear['Region'] == "CD" ].index, inplace = True)
            sSegment = "Less CD"
    elif( selSegment == '3'):
            CYear.drop(CYear[CYear['Type'] == "RIC" ].index, inplace = True)
            PYear.drop(PYear[PYear['Type'] == "RIC" ].index, inplace = True)
            BYear.drop(BYear[BYear['Region'] == "RIC" ].index, inplace = True)
            sSegment = "Less RIC"
    else:
        pass



  ### Step 3 - Select Data as per Vertical ----------------------------------
  ### =======================================================================
    LoginUser = 'All'

    if(LoginUser == "Medical"):
        CYear = CYear [ (CYear.Vertical == 'a. Medical') | (CYear.Vertical == 'b. Skincare') | (CYear.Vertical == 'g. CD') ]
        PYear = PYear [ (PYear.Vertical == 'a. Medical') | (PYear.Vertical == 'b. Skincare') | (PYear.Vertical == 'g. CD')]
        BYear = BYear [ (BYear.Department == 'MED') | (BYear.Department == 'SKI') | (BYear.Region == 'CD')]
    if(LoginUser == "Equip"):
        CYear = CYear [ (CYear.Vertical == 'c. Equip') | (CYear.Vertical == 'd. Tech')  | (CYear.Vertical == 'g. CD') ]
        PYear = PYear [ (PYear.Vertical == 'c. Equip') | (PYear.Vertical == 'd. Tech') | (PYear.Vertical == 'g. CD') ]
        BYear = BYear [ (BYear.Department == 'EQU') | (BYear.Department == 'TEC') | (BYear.Region == 'CD')]
    elif(LoginUser == "Dental"):
        CYear = CYear [CYear.Vertical == 'e. Dental']
        PYear = PYear [PYear.Vertical == 'e. Dental']
        BYear = BYear [BYear.Department == 'DEN']
    else:
        CYear = CYear
        PYear = PYear
        BYear = BYear



  ### Step 4 - Select Report Data -------------------------------------------
  ### =======================================================================

    # Define Month Number and Month Name
    M1 = '1'
    MS2 = '12';  M2 = int(MS2)+1;   M2 = str(M2)
    M3 = MS2

    monthName = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', 
            '10':'October', '11':'November', '12':'December'}

    List = []
    for i in range(int(M1), int(M2)):
            Mon = monthName[str(i)]
            List.append(Mon)

    reportingMonth = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June',
                    '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December',
                    '13':'YTD February', '14':'YTD March', '15':'YTD Apirl', '16':'YTD May', '17':'YTD June', '18':'YTD July',
                    '19':'YTD August', '20':'TYD September', '21':'YTD October', '22':'YTD November', '23':'YTD December', }
    rMonth = reportingMonth[M1]
    rMonth = reportingMonth[M2]



   ## 4a. Select Data as per Selected Month
   ## .......................................................................
    CYear = CYear[CYear.Month.isin(List)]
    PYear = PYear[PYear.Month.isin(List)]
    BYear = BYear[BYear.Month.isin(List)]



  ### Step 5 - Cleaning the Budget File -------------------------------------
  ### =======================================================================


   ## 5a. Drop the Cost Center in Budgeted DataFrame
   ## .......................................................................
    costCenter = ['LOG','FIN','HRM','ITD','ADM','MAR','TRA','ODE']
    profitCenter = ['MED','EQU', 'SKI', 'TEC', 'DEN', 'OVE']
    BYear = BYear[~BYear['Department'].isin(costCenter)]


   ## 5b. Load File Having Standard Names
   ## .......................................................................

    # Load Country and Vertical Name File for Country
    counColumns = ['Country','couForSales']
    counName = pd.read_excel("Data/couAndVerName.xlsx", sheet_name="Country" ,usecols = counColumns)

    # Load Country and Vertical Name File for Vertical
    vertColumns = ['Department','verForSales']
    VertName = pd.read_excel("Data/couAndVerName.xlsx", sheet_name="Vertical" ,usecols = vertColumns)



  ### Step 6 - Create Departmentwise Pivot Table ----------------------------
  ### =======================================================================
    CY_SalbyVer = pd.pivot_table(CYear,index=["Vertical","Country"],aggfunc=np.sum, margins=True, margins_name='i. Total') 
    PY_SalbyVer = pd.pivot_table(PYear,index=["Vertical","Country"],aggfunc=np.sum, margins=True, margins_name='i. Total')
    BYear = pd.pivot_table(BYear,index=["Department","Country"],aggfunc=np.sum)



  ### Step 7 - Inline Budgeted DF to Concate with Actual Sales DF -----------
  ### =======================================================================
    BYear.reset_index(inplace=True)   # to make pivot to normal DF
    BYear.rename(columns = {'1a.Revenue':'BY_Revenue', '2a.Cost of Sales':'BY_CoS'}, inplace=True)

    # Drop Rows Having Value less than 1 from DF
    BYear = BYear[BYear.BY_Revenue >= 1]

    # Map Country and Vertical Column to have Standard Country and Vertical Name
    BYearCou = pd.merge(BYear, counName,  on ='Country',  how ='inner')
    BYearVer = pd.merge(BYearCou, VertName,  on ='Department',  how ='inner')

    # Drop old Department and Country name and keep Mapped Country and Vertical Name
    BYearVer.drop(['Department', 'Country'], axis='columns', inplace=True)

    BYear = pd.pivot_table(BYearVer,index=["verForSales","couForSales"],aggfunc=np.sum, margins=True, margins_name='i. Total')



  ### Step 8 - Combine CY, PY and BY DataFrame ------------------------------
  ### =======================================================================
    Comb_SalbyVer = pd.concat([CY_SalbyVer, BYear, PY_SalbyVer], axis=1).replace(np.nan,0)
    Comb_SalbyVer.reset_index(inplace=True)

    # Drop old Department and Country name and keep Mapped Country and Vertical Name
    Comb_SalbyVer.drop(['index'], axis='columns', inplace=True)



  ### Step 9 - Create Margin ------------------------------------------------
  ### =======================================================================
    Comb_SalbyVer['CY_Margin'] = Comb_SalbyVer['CY_Revenue'] - Comb_SalbyVer['CY_CoS']
    Comb_SalbyVer['PY_Margin'] = Comb_SalbyVer['PY_Revenue'] - Comb_SalbyVer['PY_CoS']
    Comb_SalbyVer['BY_Margin'] = Comb_SalbyVer['BY_Revenue'] - Comb_SalbyVer['BY_CoS']


   ## 9a. Select column to concate later
   ## .......................................................................
    CombineIndex = Comb_SalbyVer.loc[ : , ['level_0','level_1']]
    ABC = CombineIndex



  ### Step 10 - Convert Data into Desired Currency --------------------------
  ### =======================================================================
    if(selCurrency == "LBP"):
        Comb_SalbyVer = Comb_SalbyVer.select_dtypes(exclude=['object','datetime']) * 410
    elif(selCurrency == "USD"):
        Comb_SalbyVer = Comb_SalbyVer.select_dtypes(exclude=['object','datetime']) /3.68
    elif(selCurrency == "SAR"):
        Comb_SalbyVer = Comb_SalbyVer.select_dtypes(exclude=['object','datetime']) * 0.98
    else:
        Comb_SalbyVer = Comb_SalbyVer.select_dtypes(exclude=['object','datetime'])



  ### Step 11 - Concat Combine Dataframe and Index --------------------------
  ### =======================================================================
    Combine = pd.concat([ABC, Comb_SalbyVer], axis=1).replace(np.nan,0)
    CombineVer = Combine
    CombineCou = Combine

    # to Have Country in In Order
    CombineCou['level_2'] = CombineCou['level_1']
    CombineCou.loc[CombineCou["level_2"] == "a. Medical", ["level_2"]] = "x. Medical"
    CombineCou.loc[CombineCou["level_2"] == "c. Equip", ["level_2"]] = "x. Equip"



  ### Step 12 - Create SubTotal - VerticalWise ------------------------------
  ### =======================================================================
    # for Vertical
    Amt = ['CY_CoS','CY_Revenue','CY_Margin', 'PY_CoS','PY_Revenue','PY_Margin', 'BY_CoS','BY_Revenue','BY_Margin']
    CombineVer = pd.pivot_table(CombineVer, values=Amt, index=["level_0","level_1"], fill_value=0, aggfunc=np.sum, dropna=True)
    CombineVer = pd.concat([d.append(d.sum().rename((k, 'Total'))) for k, d in CombineVer.groupby(level=0)]).append(CombineVer.sum().rename(('Grand', 'Total')))

    # for Country
    CombineCou = pd.pivot_table(CombineCou, values=Amt, index=["level_2","level_0"], fill_value=0, aggfunc=np.sum, dropna=True)
    CombineCou = pd.concat([d.append(d.sum().rename((k, 'z. Total Country'))) for k, d in CombineCou.groupby(level=0)]).append(CombineCou.sum().rename(('Grand', 'Total')))


   ## 12a. reset index to remove multi-index formate
   ## .......................................................................
    CombineVer.reset_index(inplace=True)
    CombineCou.reset_index(inplace=True)


   ## 12b. Sort Country DataFrame as per Country Wise
   ## .......................................................................
    CombineCou.loc[CombineCou["level_2"] == "", ["level_2"]] = "z. Total"
    CombineCou = CombineCou.sort_values(by=['level_2','level_0'], ascending=True)


   ## 12b. Sort Country DataFrame as per Country Wise
   ## .......................................................................
    CombineVer = CombineVer.replace(r'^.. ', '', regex=True)    # Replace "a. " with ""
    CombineVer.drop(CombineVer.tail(2).index,inplace=True)      # drop last n rows

    CombineCou = CombineCou.replace(r'^.. ', '', regex=True)    # Replace "a. " with ""
    CombineCou.drop(CombineCou.tail(1).index,inplace=True)      # drop last n rows
    CombineCou.drop(CombineCou.loc[CombineCou['level_2']=="Grand"].index, inplace=True)



  ### Step 13 - Add 0.01 in Revenue to avoid Error - for Sub-Total ----------
  ### =======================================================================

    # for Vertical
    CombineVer['BY_Revenue'] = CombineVer['BY_Revenue'] + .01 
    CombineVer['CY_Revenue'] = CombineVer['CY_Revenue'] + .01 
    CombineVer['PY_Revenue'] = CombineVer['PY_Revenue'] + .01 

    # for Country
    CombineCou['BY_Revenue'] = CombineCou['BY_Revenue'] + .01 
    CombineCou['CY_Revenue'] = CombineCou['CY_Revenue'] + .01 
    CombineCou['PY_Revenue'] = CombineCou['PY_Revenue'] + .01 



  ### Step 14 - Calculate Gross Profit - for Sub-Total ----------------------
  ### =======================================================================

    # for Vertical
    CombineVer["CY_GP"] = CombineVer["CY_Margin"] / CombineVer["CY_Revenue"]
    CombineVer["PY_GP"] = CombineVer["PY_Margin"] / CombineVer["PY_Revenue"]
    CombineVer["BY_GP"] = CombineVer["BY_Margin"] / CombineVer["BY_Revenue"]

    # for Country
    CombineCou["CY_GP"] = CombineCou["CY_Margin"] / CombineCou["CY_Revenue"]
    CombineCou["PY_GP"] = CombineCou["PY_Margin"] / CombineCou["PY_Revenue"]
    CombineCou["BY_GP"] = CombineCou["BY_Margin"] / CombineCou["BY_Revenue"]

    CombineVer["New"] = "hideRow001"
    CombineVer.loc[CombineVer["level_1"] == "Total", ["New"]] = CombineVer["level_0"]
    CombineVer.loc[CombineVer["level_1"] == "", ["New"]] = "Grand Tot"
    CombineVer.loc[CombineVer["level_1"] == "", ["level_1"]] = "Grand Tot"

    CombineCou["New"] = "hideRow001"
    CombineCou.loc[CombineCou["level_0"] == "Total Country", ["New"]] = CombineCou["level_2"]



  ### Step 15 - Create Graph Data ------------------------------------------
  ### =======================================================================
    df1 = pd.DataFrame([['Medical', 0], ['Skincare', 0], ['Equip', 0], ['Tech', 0], ['Dental', 0]],columns=['level_0', 'dummy'])
    df1 = df1.set_index('level_0')
    df = CombineVer.loc[(CombineVer['level_1'] == 'Total') | (CombineVer['level_1'] == 'Grand Tot') ]
    df = df.set_index('level_0')
    grap = pd.concat([df, df1], axis=1).replace(np.nan,0)

    medAct = grap.loc['Medical', 'CY_Revenue']
    medBdg = grap.loc['Medical', 'BY_Revenue']
    medPre = grap.loc['Medical', 'PY_Revenue']
    skiAct = grap.loc['Skincare', 'CY_Revenue']
    skiBdg = grap.loc['Skincare', 'BY_Revenue']
    skiPre = grap.loc['Skincare', 'PY_Revenue']
    equAct = grap.loc['Equip', 'CY_Revenue']
    equBdg = grap.loc['Equip', 'BY_Revenue']
    equPre = grap.loc['Equip', 'PY_Revenue']
    tecAct = grap.loc['Tech', 'CY_Revenue']
    tecBdg = grap.loc['Tech', 'BY_Revenue']
    tecPre = grap.loc['Tech', 'PY_Revenue']
    denAct = grap.loc['Dental', 'CY_Revenue']
    denBdg = grap.loc['Dental', 'BY_Revenue']
    denPre = grap.loc['Dental', 'PY_Revenue']
    totAct = grap.loc['Total', 'CY_Revenue']
    totBdg = grap.loc['Total', 'BY_Revenue']
    totPre = grap.loc['Total', 'PY_Revenue']

    othAct = totAct-medAct-skiAct-equAct-tecAct-denAct
    othBdg = totBdg-medBdg-skiBdg-equBdg-tecBdg-denBdg
    othPre = totPre-medPre-skiPre-equPre-tecPre-denPre
    perAch = totAct/totBdg



  ### Step 15 - Create Graph Data ------------------------------------------
  ### =======================================================================

    # for Vertical
    DataVer=[]
    for i in range(CombineVer.shape[0]):
        temp=CombineVer.iloc[i]
        DataVer.append(dict(temp))

    # for Country
    DataCou=[]
    for i in range(CombineCou.shape[0]):
        temp=CombineCou.iloc[i]
        DataCou.append(dict(temp))


    context = {'DataVer':DataVer, 'DataCou':DataCou }
    return render(request, 'F1_Sales/f1_SalesAnalysis.html', context)
