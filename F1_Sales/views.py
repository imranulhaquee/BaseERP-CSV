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


def showQuot(request): #URL--

  ###---- Standard Code to load Data ----------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])

  ###---- Read Quotation Basiv File -------------------------------------------------
    req_cols = ['id','qotRef','qotDat','cusName', 'qotTax', 'qotTAT','spName','opnClo']
    fPath = "Data/"+Year+"/F1_Sales/Quotations/qotBasic.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    df = df.drop(df.index[0])

    ###Convert Customer Data Frame into Python List---------------------------------------
    #dfSalA = dfSal.set_index('cusCode') # set CusCode As Index
    #data_dict = dfSalA['cusName'].to_dict() # Convert the DataFrame to a dictionary
    #DataA.customer = DataA.customer.map(data_dict).fillna(0) ### map to lookup data_dict
    
    ###Copy customer code where customer is NaN
    #DataA.loc[DataA["customer"] == 0, ["customer"]] = DataA["cusCode"]
    #DataA["customer"] = DataA["customer"].apply(lambda x: str(x) + '-' if isinstance(x, (int, float)) else x)

    ### remove duplicate rows and keep only the last occurrence subequently if that customer Code added
    ### will show because keep last record will not have 'Delete' in comment column
    #DataA = DataA.drop_duplicates(subset=['qotRef'], keep='last')
    #DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)


    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = df.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def refreshQuot(request): #URL--
    #(Get Quotation detail from DataBase and Save into Excel file )

    ###---- Qutation open/Close File to Get Last Quotation Number ---------------
    DataA = pd.read_sql('''SELECT * FROM "F1_Sales_qotBasic" ''', con=engine).fillna(0)


    ###---- Step 2 - Create a "Quotation" Folder inside "Data/F1_Sales" Folder --
    data_folder = "Data/F1_Sales"
    sales_folder = "Quotation"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass


    #Step 3 - Save Customer Master File as CSV File ---------------------------
    DataA['comment'] = ''
    DataA.to_csv('Data/F1_Sales/Quotation/salQuot2023.csv',index=False)

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sQuotAdd(request):
    
  ###---- Standard Code to load Data ----------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
  
  ### Qutation File to Get Last Quotation Number ----------------------
    try: 
        req_cols = ['qotRef', 'qotDat']
        fPath = "Data/"+ Year+"/F1_Sales/Quotations/qotBasic.csv"
        df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')
    except:
        data = {'qotRef': [0]}
        df = pd.DataFrame(data)
    
  ### Step 1a - Get the last Quotation No make it 5 digit & add year---
    lastQuot = df['qotRef'].max()


    context = {'lastQuot': lastQuot }
    return render(request, 'F1_Sales/sQuotAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sQuotAddUrl(request):

  ###---- Standard Code to load Data ----------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])

 
  # Save Quotation Basic Data -------------------------------------------
  # ----------------------------------------------------------------Start
    basData = request.data[0]
    basicData = {'ID': basData['qotRef'],       'qotRef': basData['qotRef'],
              'qotDat': basData['qotDat'],   'cusCode': basData['cusCode'],
              'cusName': basData['cusName'], 'qotTBD':basData['qotTBD'], 
              'qotTAD': basData['qotTAD'],   'qotTax': basData['qotTax'],
              'qotTAT': basData['qotTAT'],	 'shipTo':  basData['shipTo'],	
              'qotComm': basData['qotComm'], 'salPer': basData['salPer'],
              'spName': basData['spName'],   'opeClo': 'Open',
              'traDate': basData['traDate'], 'comment': ''
            }

    dfBasic = pd.DataFrame(basicData, index=[0])
    fPath = fPath = "Data/"+ Year+"/F1_Sales/Quotations/qotBasic.csv"
    dfBasic.to_csv(fPath, index=False, header=False, mode='a')


  # Save Quotation Additional Data --------------------------------------
  # ----------------------------------------------------------------Start
    addiData = request.data[1]
    lastN = 1
    for data in addiData:
      if( data['id'] == '0'):
        lastN=lastN+1
        ID = lastN
      else:
        ID = data['id']

      addiData={'ID': basData['qotRef'], 'qotRef': basData['qotRef'], 'sno':data['sno'],
              'itmCod':data['itmcode'], 'desc':data['desc'], 'qty':data['qty'],
              'price':data['price'], 'disc':data['price'], 'tot':data ['tot'],
              'traDate':basData['traDate'], 'action':'' 
              }
    
      dfAddi = pd.DataFrame(addiData, index=[0])
      fPath = fPath = "Data/"+ Year+"/F1_Sales/Quotations/qotAddi.csv"
      dfAddi.to_csv(fPath, index=False, header=False, mode='a')

  
    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sQuotEdit(request, pk):
    print(pk)
    #(to Show Quotation to edit)

    Basic = qotBasic.objects.get(id=pk)
    serilizerA = qotBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    quotBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = qotAddiSerializer(QotAddi, many=True) ### Serialize the selected data
    quotAddiItems = serilizerB.data ### Get the data not attributes
    quotAddiItems = [dict(item) for item in quotAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    quotAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in quotAddiItems]

    context = {'lastQuot': pk, 'qBasic':quotBasi,  'addiQuote':quotAddiItems}
    return render(request, 'F1_Sales/sQuotEdit.html', context)


def sQuotEditFetch(request, pk):
    Basic = qotBasic.objects.get(id=pk)
    serilizerA = qotBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    quotBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = qotAddiSerializer(QotAddi, many=True) ### Serialize the selected data
    quotAddiItems = serilizerB.data ### Get the data not attributes
    quotAddiItems = [dict(item) for item in quotAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    quotAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in quotAddiItems]

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([quotBasi, quotAddiItems], safe=False) 


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delQot(request, pk):

 #----------Delete Record -----------------------------------------------
      QotBasic = qotBasic.objects.get(id=pk)
      
      pk = int(pk)
      QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Filter  'id' of all record and convert into list
      #id_list = [record.id for record in QotAddi]  ### Get 'id' of all record and convert into list

      with transaction.atomic():
        for data in QotAddi:
          data.delete()
      
      QotBasic.delete()


      ###Variable to Save in CSV File ..........
      tempDf = {'id': pk, 
                'qotRef': pk,
                'qotDat': '', 
                'cusCode': '',
                'qotTBD': '' , 
                'qotTAD':'',
                'qotTax': '',
                'qotTAT': '',	
                'shipTo': '',	
                'qotComm': '',	
                'salPer': '',
                'opnClo': '',
                'comment': 'Delete',
              }

      df = pd.DataFrame(tempDf, index=[0])
      df.to_csv('Data/F1_Sales/Quotation/salQuot2023.csv',index=False, header=False, mode='a')
      
      return Response('Items delete successfully!')


def showQuotSum(request):
    ###---- Read Quotation File 'with Specific Column' -----------------
    req_cols = ['qotRef','qotDat', 'cusCode', 'cusName', 'opnClo', 'comment']
    dfSal = pd.read_csv("Data/F1_Sales/Quotation/salQuot2023.csv", usecols=req_cols).fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = dfSal.drop_duplicates(subset=['qotRef'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)
    DataB = DataB.drop('comment', axis=1)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 



def sQuotPdf(request):
  #----------Get Data from html Page and convert into list---------------
    pk1 = request.GET.get('query_name')
    pk = int(pk1)

  ###---- Standard Code to load Data ----------------------------------
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])

  ###---- Read Quotation Basic CSV File -------------------------------
    fPath = "Data/"+Year+"/F1_Sales/Quotations/qotBasic.csv"
    dfA = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfA = dfA.drop(dfA.index[0])
    dfBasic = dfA[dfA['id'] == pk].fillna(0) ### Filter
    quotBasi = dfBasic.to_dict(orient="records") ### convert into dictionary

  ###---- Read Quotation Basic CSV File -------------------------------
    fPath = "Data/"+Year+"/F1_Sales/Quotations/qotAddi.csv"
    dfB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')
    dfAddi = dfB[dfB['qotRef'] == pk].fillna(0) ### Filter
    quotAddiItems = dfAddi.to_dict(orient="records") ### convert into dictionary

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



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Quotation -COST ☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sQotCotAdd(request, pk):
  ### Step 1 - Read Item Salece Price---------------------------------------------
  ### ----------------------------------------------------------------------------
    req_Column = ['itmCode', 'uPrice']
    SP = pd.read_csv("Data/H1_Items/Item/ItemSalPrice.csv", usecols=req_Column ,encoding='unicode_escape').fillna(0)
    SP = SP.drop_duplicates(subset=['itmCode'], keep='last')
    SP = SP.to_dict(orient="records")   ### Convert Data into Dictionary
    SPList = {item['itmCode']: item['uPrice'] for item in SP} # Extract desired values into a new dictionary


  ### Step 2 - Read Sales Quote Basic for Employee -------------------------------
  ### ----------------------------------------------------------------------------
    queryBasic = f'SELECT * FROM "F1_Sales_qotBasic" WHERE qotRef = {pk}'
    qotBasic = pd.read_sql(queryBasic, con=engine)
    empCode = int(qotBasic['salPer'][0]) #get employee code
    qotBasi = qotBasic.to_dict(orient="records") ### into Dictionary

  ### Step 3 - Read Employee Cost ------------------------------------------------
  ### ----------------------------------------------------------------------------
    req_Column = ['empCode', 'itemCode', 'salCostPU']
    empCost = pd.read_csv("Data/2023/I1_Hrm/Employees/empTargetDetail.csv", usecols=req_Column ,encoding='unicode_escape').fillna(0)
    empCost = empCost.loc[empCost['empCode'] == empCode]
    empCost = empCost.to_dict(orient="records")   ### Convert Data into Dictionary
    empCostList = {item['itemCode']: item['salCostPU'] for item in empCost} # Extract desired values into a new dictionary


  ### Step 4 - Read Sales Quote Additional ---------------------------------------
  ### ----------------------------------------------------------------------------
    DataA = pd.read_sql('''SELECT * FROM "F1_Sales_qotAddi" ''', con=engine).fillna(0)
    query = f'SELECT * FROM "F1_Sales_qotAddi" WHERE qotRef = {pk}'
    qotAddi = pd.read_sql(query, con=engine)
    qotAddi['itmCode'] = qotAddi['itmCode'].astype(int)

    ### Step 4.1 - MAP the List to Creat Columne ---------------------------------
    qotAddi['ItemCost'] = qotAddi['itmCode'].map(SPList).fillna(0)
    qotAddi['EmpCost'] = qotAddi['itmCode'].map(empCostList).fillna(0)

    qotAddiItems = qotAddi.to_dict(orient="records")  ### into Dictionary

    context = {'lastOrder': pk, 'oBasic':qotBasi,  'addiOrder':qotAddiItems}
    return render(request, 'F1_Sales/sQotCotAdd.html', context)



    # Basic = qotBasic.objects.get(id=pk)
    # serilizerA = qotBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # # if there is 'None' cell convert into '' empty to avoid error in JS 
    # qotBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    # QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Get all record where 'qotRef = pk (value)'
    # serilizerB = qotAddiSerializer(QotAddi, many=True) ### Serialize the selected data
    # qotAddiItems = serilizerB.data ### Get the data not attributes
    # qotAddiItems = [dict(item) for item in qotAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    # qotAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in qotAddiItems]

    # context = {'lastOrder': pk, 'oBasic':qotBasi,  'addiOrder':qotAddiItems}
    # return render(request, 'F1_Sales/sQotCotAdd.html', context)






#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Sales Order ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sOrderList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sOrderList.html', context)

def showOrderURL(request):
    #(Get Sales Order Detail from DataBase)

    ###---- Qutation open/Close File to Get Last Quotation Number -------------
    query = '''SELECT "soRef","soDat", "cusName", "soTax", "soTAT", "spName", "opnClo" , "qotRef" FROM "F1_Sales_soBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = dfSal.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 


def sOrderAdd(request):
    #(to Show Sales Order Addition Page)

    ###---- Sales Order File to Get Last Quotation Number -------------
    Max = '''SELECT MAX(id) FROM "F1_Sales_soBasic"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(20230000, inplace=True)
    lastOrder= val.loc[0, 'new']


    context = {'lastOrder': lastOrder }
    return render(request, 'F1_Sales/sOrderAdd.html', context)


def openSalQotURL(request):
    ###---- Get all Sales Quotation ----------------------------------------------------------------
    query = '''SELECT "qotRef","qotDat", "cusCode", "cusName", "opnClo" FROM "F1_Sales_qotBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ###---- Get all Sales Order "qotRef" -----------------------------------------------------------
    queryB = '''SELECT "QotRef" FROM "F1_Sales_soBasic"'''
    dfSO = pd.read_sql(queryB, con=engine)
    soList = dfSO['qotRef'].tolist() #Convert "qotRef" column into list

    ### Step 2 - Filter out Sales Order-----------------------------
    Data = dfSal[dfSal['opnClo'] != 'Closed']
    filterData = Data[~Data['qotRef'].isin(soList)]

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = filterData.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sOrderAddUrl(request):
    #(to Save Quotation into Database)

    #---- Quotation Basic Information ---------------------------------------
    basData = request.data[0]
    SoBasic=soBasic(basData['soRef'], basData['soRef'], basData['soDat'],
                    basData['cusCode'], basData['cusName'],basData['soTBD'],
                    basData['soTAD'], basData['soTax'], basData['soTAT'], basData['shipTo'],
                    basData['soComm'], "Open", basData['spName'], basData['salPer'],
                    basData['qotRef'], basData['qotDat'])
    SoBasic.save()

    #---- Quotation Transaction ---------------------------------------------
    addiData = request.data[1]
    Max = '''SELECT MAX(id) FROM "F1_Sales_soAddi"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(0, inplace=True) # if there is no record put 0
    lastN = val.loc[0, 'new']

    with transaction.atomic():
      for data in addiData:
          if( data['id'] == '0'):
            lastN=lastN+1
            ID = lastN
          else:
            ID = data['id']

          value = soAddi(ID, basData['soRef'], data ['sno'],data ['itmcode'], data ['desc'], data ['qty'],data ['price'], data ['disc'], data ['tot'])
          value.save()

    #-- Delete Missing IDs from DataBase ------------------------------
    missingId = request.data[2]
    queryset = soAddi.objects.filter(id__in=missingId)
    queryset.delete()


    ###---Change Sales Order Status as Closed ------------------
    rec = basData['qotRef']
    record = qotBasic.objects.get(id=rec)   
    record.opnClo = 'Closed' # Update the specific field
    record.save() # Save the changes to the database


    #Variable to Save in CSV File ..........
    tempDf = {'ID': basData['soRef'], 
              'soRef': basData['soRef'],
              'soDat': basData['soDat'], 
              'cusCode': basData['cusCode'],
              'cusName': basData['cusName'],
              'soTBD':basData['soTBD'], 
              'soTAD': basData['soTAD'],
              'soTax': basData['soTax'],
              'soTAT': basData['soTAT'],	
              'shipTo':  basData['shipTo'],	
              'soComm': basData['soComm'],
              'opnClo': 'Open',
              'spName': basData['spName'],
              'spCode': basData['salPer'],
              'qotRef': basData['qotRef'],
              'qotDat': basData['qotDat'],
              'comment': ''
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/F1_Sales/SalesOrder/salOrder2023.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sOrderEdit(request, pk):
    print(pk)
    #(to Show Quotation to edit)

    Basic = soBasic.objects.get(id=pk)
    serilizerA = soBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    soBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    SoAddi = soAddi.objects.filter(soRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = soAddiSerializer(SoAddi, many=True) ### Serialize the selected data
    soAddiItems = serilizerB.data ### Get the data not attributes
    soAddiItems = [dict(item) for item in soAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    soAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in soAddiItems]

    context = {'lastOrder': pk, 'oBasic':soBasi,  'addiOrder':soAddiItems}
    return render(request, 'F1_Sales/sOrderEdit.html', context)


def sOrderEditFetch(request, pk):  # to Bring Quotation Detail....................
    Basic = qotBasic.objects.get(id=pk)
    serilizerA = qotBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    quotBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = qotAddiSerializer(QotAddi, many=True) ### Serialize the selected data
    quotAddiItems = serilizerB.data ### Get the data not attributes
    quotAddiItems = [dict(item) for item in quotAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    quotAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in quotAddiItems]

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([quotBasi, quotAddiItems], safe=False) 


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delSOrd(request, pk, Qot):

 #----------Delete Record -----------------------------------------------
      SoBasic = soBasic.objects.get(id=pk)
      SoBasic.delete()
      
      pk = int(pk)
      SoAddi = soAddi.objects.filter(soRef=pk)  ### Filter  'id' of all record and convert into list

      with transaction.atomic():
        for data in SoAddi:
          data.delete()
      
      ###---Change Sales Quotation Status as Open on delete relevent Sales Order ------
      record = qotBasic.objects.get(id=Qot)   
      record.opnClo = 'Open' # Update the specific field
      record.save() # Save the changes to the database

      return Response('Items delete successfully!')




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Delivery Notes ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sDeliveryList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sDeliveryList.html', context)


def showDeliveryURL(request):
    #(Get Sales Order Detail from DataBase)

    ###---- Qutation open/Close File to Get Last Quotation Number -------------
    query = '''SELECT "dlRef","dlDat", "cusName", "dlTax", "dlTAT", "spName", "opnClo" , "soRef" FROM "F1_Sales_dlBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = dfSal.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 



def openSalDlURL(request):  #Get the list of all Open Sales Order only .........
    ###---- Get all Sales Order ----------------------------------------------------------------
    query = '''SELECT "soRef","soDat", "cusCode", "cusName", "opnClo" FROM "F1_Sales_soBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ###---- Get all Delivery Notes "dfRef" -----------------------------------------------------------
    queryB = '''SELECT "soRef" FROM "F1_Sales_dlBasic"'''
    dfDl = pd.read_sql(queryB, con=engine)
    soList = dfDl['soRef'].tolist() #Convert "qotRef" column into list

    ### Step 2 - Filter out Delivery Note -----------------------------------------------
    Data = dfSal[dfSal['opnClo'] != 'Closed']
    filterData = Data[~Data['soRef'].isin(soList)]

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = filterData.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def sOrderDetailURL(request, pk):  #Fetch Sales Order Detail for initially load .....
    Basic = soBasic.objects.get(id=pk)
    serilizerA = soBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    soBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    SoAddi = soAddi.objects.filter(soRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = soAddiSerializer(SoAddi, many=True) ### Serialize the selected data
    soAddiItems = serilizerB.data ### Get the data not attributes
    soAddiItems = [dict(item) for item in soAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    soAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in soAddiItems]

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([soBasi, soAddiItems], safe=False) 



def sDeliveryAdd(request):
    #(to Show Sales Order Addition Page)

    ###---- Sales Order File to Get Last Quotation Number -------------
    Max = '''SELECT MAX(id) FROM "F1_Sales_dlBasic"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(20230000, inplace=True)
    lastDelivery= val.loc[0, 'new']


    context = {'lastDelivery': lastDelivery }
    return render(request, 'F1_Sales/sDeliveryAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sDeliveryAddURL(request):
    #(to Save Quotation into Database)

    #print(request.data)
    #---- Quotation Basic Information ---------------------------------------
    basData = request.data[0]
    DlBasic=dlBasic(basData['dlRef'], basData['dlRef'], basData['dlDat'],
                    basData['cusCode'], basData['cusName'],basData['dlTBD'],
                    basData['dlTAD'], basData['dlTax'], basData['dlTAT'], basData['shipTo'],
                    basData['dlComm'], "Open", basData['spName'], basData['salPer'],
                    basData['soRef'], basData['soDat'])
    DlBasic.save()

    #---- Delevery Last Transaction ------------------------------------------
    addiData = request.data[1]
    Max = '''SELECT MAX(id) FROM "F1_Sales_dlAddi"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(0, inplace=True) # if there is no record put 0
    lastN = val.loc[0, 'new']

    #---- Item Last Transaction ------------------------------------------
    MaxItem = '''SELECT MAX(id) FROM "H1_Items_itmLedger"'''
    df3 = pd.read_sql(MaxItem, con=engine)
    itmVal = df3.rename(columns={df3.columns[0]: 'new'})
    itmVal.fillna(0, inplace=True) # if there is no record put 0
    lastItmN = itmVal.loc[0, 'new']
    lastItmN

    with transaction.atomic():
      for data in addiData:
          if( data['id'] == '0'):
            lastN=lastN+1
            ID = lastN
          else:
            ID = data['id']

          value = dlAddi(ID, basData['dlRef'], data ['sno'],data ['itmcode'], data ['desc'], data ['qty'],data ['price'], data ['disc'], data ['tot'])
          value.save()

          # Item Ledger Entry
          lastItmN=lastItmN+1
          qtyPU = int(data['qty'])*-1
          cost = int(data ['price'])*.6
          item = itmLedger(lastItmN , data['itmcode'], data['desc'], basData['dlDat'], 1, cost, qtyPU, 0, 0, 'Sales of Item to'+basData['cusName']  )
          item.save()  # Save the record to the database


    #-- Delete Missing IDs from DataBase ------------------------------
    missingId = request.data[2]
    queryset = soAddi.objects.filter(id__in=missingId)
    queryset.delete()


    ###---Change Sales Order Status as Closed ------------------
    rec = basData['soRef']
    record = soBasic.objects.get(id=rec)   
    record.opnClo = 'Closed' # Update the specific field
    record.save() # Save the changes to the database


    #Variable to Save in CSV File ..........
    tempDf = {'ID': basData['dlRef'], 
              'dlRef': basData['dlRef'],
              'dlDat': basData['dlDat'], 
              'cusCode': basData['cusCode'],
              'cusName': basData['cusName'],
              'dlTBD':basData['dlTBD'], 
              'dlTAD': basData['dlTAD'],
              'dlTax': basData['dlTax'],
              'dlTAT': basData['dlTAT'],	
              'shipTo':  basData['shipTo'],	
              'dlComm': basData['dlComm'],
              'opnClo': 'Open',
              'spName': basData['spName'],
              'spCode': basData['salPer'],
              'soRef': basData['soRef'],
              'soDat': basData['soDat'],
              'comment': ''
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/F1_Sales/sDelivery/sDelivery2023.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sDeliveryEdit(request, pk):
    print(pk)
    #(to Show Quotation to edit)

    Basic = dlBasic.objects.get(id=pk)
    serilizerA = dlBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    dlBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    DlAddi = dlAddi.objects.filter(dlRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = dlAddiSerializer(DlAddi, many=True) ### Serialize the selected data
    dlAddiItems = serilizerB.data ### Get the data not attributes
    dlAddiItems = [dict(item) for item in dlAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    dlAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in dlAddiItems]

    context = {'lastOrder': pk, 'dlBasic':dlBasi,  'dlAddiItems':dlAddiItems}
    return render(request, 'F1_Sales/sDeliveryEdit.html', context)


def sDeliveryEditFetch(request, pk):  # to Bring Quotation Detail....................
    Basic = qotBasic.objects.get(id=pk)
    serilizerA = qotBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    quotBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    QotAddi = qotAddi.objects.filter(qotRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = qotAddiSerializer(QotAddi, many=True) ### Serialize the selected data
    quotAddiItems = serilizerB.data ### Get the data not attributes
    quotAddiItems = [dict(item) for item in quotAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    quotAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in quotAddiItems]

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([quotBasi, quotAddiItems], safe=False) 



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delDelivery(request, pk, So):

 #----------Delete Record -----------------------------------------------
      DlBasic = dlBasic.objects.get(id=pk)
      DlBasic.delete()
      
      pk = int(pk)
      DlAddi = dlAddi.objects.filter(dlRef=pk)  ### Filter  'id' of all record and convert into list

      with transaction.atomic():
        for data in DlAddi:
          data.delete()
      
      ###---Change Sales Quotation Status as Open on delete relevent Sales Order ------
      record = soBasic.objects.get(id=So)   
      record.opnClo = 'Open' # Update the specific field
      record.save() # Save the changes to the database

      return Response('Items delete successfully!')





#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Delivery Notes ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def sInvoiceList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'F1_Sales/sInvoiceList.html', context)


def showInvoiceURL(request):
    #(Get Sales Order Detail from DataBase)

    ###---- Qutation open/Close File to Get Last Quotation Number -------------
    query = '''SELECT "siRef","siDat", "cusName", "siTax", "siTAT", "spName", "opnClo" , "dlRef" FROM "F1_Sales_siBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = dfSal.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 



def openSalSiURL(request):  #Get the list of all Open Sales Order only .........
    ###---- Get all Sales Order ----------------------------------------------------------------
    query = '''SELECT "dlRef","dlDat", "cusCode", "cusName", "opnClo" FROM "F1_Sales_dlBasic"'''
    dfSal = pd.read_sql(query, con=engine)

    ###---- Get all Delivery Notes "dfRef" -----------------------------------------------------------
    queryB = '''SELECT "dlRef" FROM "F1_Sales_siBasic"'''
    dfDl = pd.read_sql(queryB, con=engine)
    soList = dfDl['dlRef'].tolist() #Convert "qotRef" column into list

    ### Step 2 - Filter out Delivery Note -----------------------------------------------
    Data = dfSal[dfSal['opnClo'] != 'Closed']
    filterData = Data[~Data['dlRef'].isin(soList)]

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = filterData.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def sInvoiceDetailURL(request, pk):  #Fetch Sales Order Detail for initially load .....
    Basic = dlBasic.objects.get(id=pk)
    serilizerA = dlBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    dlBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    DlAddi = dlAddi.objects.filter(dlRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = dlAddiSerializer(DlAddi, many=True) ### Serialize the selected data
    dlAddiItems = serilizerB.data ### Get the data not attributes
    dlAddiItems = [dict(item) for item in dlAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    dlAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in dlAddiItems]

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse([dlBasi, dlAddiItems], safe=False) 


def sInvoiceAdd(request):
    #(to Show Sales Order Addition Page)

    ###---- Sales Order File to Get Last Quotation Number -------------
    Max = '''SELECT MAX(id) FROM "F1_Sales_siBasic"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(20230000, inplace=True)
    lastInvoice= val.loc[0, 'new']


    context = {'lastInvoice': lastInvoice }
    return render(request, 'F1_Sales/sInvoiceAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def sInvoiceAddURL(request):
    #(to Save Quotation into Database)

    print(request.data)
    #---- Quotation Basic Information ---------------------------------------
    basData = request.data[0]
    SiBasic=siBasic(basData['siRef'], basData['siRef'], basData['siDat'],
                    basData['cusCode'], basData['cusName'],basData['siTBD'],
                    basData['siTAD'], basData['siTax'], basData['siTAT'], basData['shipTo'],
                    basData['siComm'], "Open", basData['spName'], basData['salPer'],
                    basData['dlRef'], basData['dlDat'])
    SiBasic.save()

    #---- Delevery Last Transaction ------------------------------------------
    addiData = request.data[1]
    Max = '''SELECT MAX(id) FROM "F1_Sales_siAddi"'''
    df2 = pd.read_sql(Max, con=engine)
    val = df2.rename(columns={df2.columns[0]: 'new'})
    val.fillna(0, inplace=True) # if there is no record put 0
    lastN = val.loc[0, 'new']

    with transaction.atomic():
      for data in addiData:
          if( data['id'] == '0'):
            lastN=lastN+1
            ID = lastN
          else:
            ID = data['id']

          value = siAddi(ID, basData['siRef'], data ['sno'],data ['itmcode'], data ['desc'], data ['qty'],data ['price'], data ['disc'], data ['tot'])
          value.save()

    #-- Delete Missing IDs from DataBase ------------------------------
    missingId = request.data[2]
    queryset = dlAddi.objects.filter(id__in=missingId)
    queryset.delete()


    ###---Change Sales Order Status as Closed ------------------
    rec = basData['dlRef']
    record = dlBasic.objects.get(id=rec)   
    record.opnClo = 'Closed' # Update the specific field
    record.save() # Save the changes to the database


    #Variable to Save in CSV File ..........
    tempDf = {'ID': basData['siRef'], 
              'siRef': basData['siRef'],
              'siDat': basData['siDat'], 
              'cusCode': basData['cusCode'],
              'cusName': basData['cusName'],
              'siTBD':basData['siTBD'], 
              'siTAD': basData['siTAD'],
              'siTax': basData['siTax'],
              'siTAT': basData['siTAT'],	
              'shipTo':  basData['shipTo'],	
              'siComm': basData['siComm'],
              'opnClo': 'Open',
              'spName': basData['spName'],
              'spCode': basData['salPer'],
              'dlRef': basData['dlRef'],
              'dlDat': basData['dlDat'],
              'comment': ''
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/F1_Sales/sInvoice/sInvoice2023.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



def sInvoiceEdit(request, pk):
    print(pk)
    #(to Show Quotation to edit)

    Basic = siBasic.objects.get(id=pk)
    serilizerA = siBasicSerializer(Basic, many=False) #for single record 'many=False' other wise ittiration error will come
    # if there is 'None' cell convert into '' empty to avoid error in JS 
    siBasi = {k: '' if v is None else v for k, v in serilizerA.data.items()}

    SiAddi = siAddi.objects.filter(siRef=pk)  ### Get all record where 'qotRef = pk (value)'
    serilizerB = siAddiSerializer(SiAddi, many=True) ### Serialize the selected data
    siAddiItems = serilizerB.data ### Get the data not attributes
    siAddiItems = [dict(item) for item in siAddiItems]  ### Convert OrderedDict into (0,1,2,3,etct)
    siAddiItems = [{key: '' if value is None else value for key, value in dictionary.items()} for dictionary in siAddiItems]

    context = {'lastOrder': pk, 'siBasic':siBasi,  'siAddiItems':siAddiItems}
    return render(request, 'F1_Sales/sInvoiceEdit.html', context)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delInvoice(request, pk, So):

 #----------Delete Record -----------------------------------------------
      SiBasic = siBasic.objects.get(id=pk)
      SiBasic.delete()
      
      pk = int(pk)
      SiAddi = siAddi.objects.filter(siRef=pk)  ### Filter  'id' of all record and convert into list

      with transaction.atomic():
        for data in SiAddi:
          data.delete()
      
      ###---Change Sales Quotation Status as Open on delete relevent Sales Order ------
      record = dlBasic.objects.get(id=So)   
      record.opnClo = 'Open' # Update the specific field
      record.save() # Save the changes to the database

      return Response('Items delete successfully!')





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
