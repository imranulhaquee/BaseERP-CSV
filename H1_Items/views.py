from django.shortcuts import render, redirect, HttpResponse
import os

from H1_Items.models import itmBasic, itmExtra, itmLedger

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
from .resources import itmBasicResource, itmExtraResource
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload


### Data Base and Serializers ----------------------------
from H1_Items.serializers import itmBasicSerializer, itmExtraSerializer, itmInitSerializer, itmLedger


import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')




# Create your views here.

#☰☰☰ ITEMS Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aItemsModule(request):
    context = {'abc':'abc', }
    return render(request, 'H1_Items/aItemsModule.html', context)




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Item Master Data ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aItemList(request):
    #(Supplier Main Page)
    context = {'basData':'basData' }
    return render(request, 'H1_Items/aItemList.html', context)


def aItmRefresh(request):

  ### Step 1 - Read Data from SQL--------------------------------------------
  ### =======================================================================
    basic = pd.read_sql('''SELECT * FROM "H1_Items_itmBasic" ''', con=engine)
    Extra = pd.read_sql('''SELECT * FROM "H1_Items_itmExtra" ''', con=engine)


  ### Step 2 - Merge "Basic & Extra" Dataframe by Items ID----------------
  ### =======================================================================
    Combined = pd.merge(basic, Extra, on=["itmCode"])
    Combined = Combined.drop("id_y", axis=1)
    Combined = Combined.rename(columns={'id_x': 'id'})

    Combined['comment'] = ''


  ### Step Step 3 - Create a "Item" Folder inside "Data/H1_Item" Folder-
  ### =======================================================================
    data_folder = "Data/H1_Items"
    items_folder = "Item"

    if not os.path.exists(os.path.join(data_folder, items_folder)):
        os.makedirs(os.path.join(data_folder, items_folder))
    else:
        pass


  ### Step 4 - Save Supplier Master File as CSV File ------------------------
  ### =======================================================================
    #https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
    Combined.to_csv('Data/H1_Items/Item/ItemMaster.csv',index = False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def showItem(request):
    #(Show the Detail Supplier Information)

    ### Read CSV Files in Pandas...........................
    df = pd.read_csv("Data/H1_Items/Item/ItemMaster.csv").fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = df.drop_duplicates(subset=['itmCode'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ### Convert Data into Json Dictionary..................
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def itmSelInfo(request):

    ###---- Customer Master File to Get Last Quotation Number -------------
    req_cols = ['itmCode','itmName', 'uPrice', 'comment']
    df = pd.read_csv("Data/H1_Items/Item/ItemMaster.csv", usecols=req_cols).fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = df.drop_duplicates(subset=['itmCode'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)
    DataB = DataB.drop('comment', axis=1)

    ### Convert Data into Json Dictionary..................
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 




@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def itmBasInfo(request):
    #(Get Specific column from Customer Basic DataTable)

    Detail = itmBasic.objects.only('id', 'itmCode', 'itmName') 
    serilizer = itmInitSerializer(Detail, many=True)
    return Response(serilizer.data)


#☰☰☰ ADD ITEMS ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def addItem(request):
    #(Screen to Add New Cutomer)
    context = {'Data':'Data' }
    return render(request, 'H1_Items/addItem.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def addItm(request):
    Data = request.data

    print(Data)
    
    #---- Item Basic Information ---------------------------------------
    itemBasic = itmBasic (Data['id'], Data['itmCode'],Data['itmName'],
                              Data['opeQty'], 0 , Data['itmActive'],)
    itemBasic.save()

    #---- Item Extra Information ---------------------------------------
    itemExt = itmExtra (  Data['id'], Data['itmCode'], Data['itmLogo'], Data['uPrice'], 
                              Data['brand'], Data['supplier'], Data['barCode'], 
                              Data['uom'], Data['min'], Data['max'], 
                              Data['roQty'], Data['discount'], Data['taxable'], 
                              Data['input'], Data['output'], Data['bisUnit'], 
                              Data['itmType'], Data['expiry'], Data['ref'],
                            )
    itemExt.save()

    #Variable to Save in CSV File ..........
    tempDf = {'id':  Data['itmCode'], 
              'itmCode': Data['itmCode'],
              'itmName': Data['itmName'], 
              'opeQty': Data['opeQty'],
              'cloQty':0 , 
              'itmActive': Data['itmActive'],
              'itmLogo': '',
              'uPrice': Data['uPrice'],	
              'brand': Data['brand'],	
              'supplier': Data['supplier'],	
              'barCode': Data['barCode'],
              'uom': Data['uom'],
              'min': Data['min'],	
              'max': Data['max'],
              'roQty': Data['roQty'],
              'discount': Data['discount'],	
              'taxable': Data['taxable'],	
              'input': Data['input'],
              'output': Data['output'],
              'bisUnit': Data['bisUnit'],
              'itmType': Data['itmType'],
              'expiry': Data['expiry'],
              'ref': Data['ref'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/H1_Items/Item/ItemMaster.csv',index=False, header=False, mode='a')
    #df.to_csv('Data/G1_Purchases/Customer/tempCust.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



#☰☰☰ EDIT ITEMS ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def aEditItem(request, pk):

    ItmBasic = itmBasic.objects.get(id=pk)
    ItmExtra = itmExtra.objects.get(id=pk)
    #print(ItmBasic.itmCode)

    serBasic = itmBasicSerializer(ItmBasic, many=False)
    serExtra = itmExtraSerializer(ItmExtra, many=False)
    #print(serExtra.data)

    ser_Basic = {k: '' if v is None else v for k, v in serBasic.data.items()}
    ser_Extra = {k: '' if v is None else v for k, v in serExtra.data.items()}

    #(Screen to Add New Item)
    context = {'DataA':ser_Basic, 'DataB':ser_Extra,}
    return render(request, 'H1_Items/aEditItem.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def editItm(request):
    
    Data = request.data
    emp = itmExtra.objects.get(id=Data['id'])
    #print(Data)
    
    #---- Item Basic Information ---------------------------------------
    itemBasic = itmBasic (Data['id'], Data['itmCode'],Data['itmName'],
                              Data['opeQty'], 0 , Data['itmActive'],)
    itemBasic.save()


    #---- Item Extra Information ---------------------------------------
    itemExt = itmExtra (  Data['id'], Data['itmCode'], Data['itmLogo'], Data['uPrice'], 
                              Data['brand'], Data['supplier'], Data['barCode'], 
                              Data['uom'], Data['min'], Data['max'], 
                              Data['roQty'], Data['discount'], Data['taxable'], 
                              Data['input'], Data['output'], Data['bisUnit'], 
                              Data['itmType'], Data['expiry'], Data['ref'],
                            )


    img = Data['itmLogo'] #will return sting incase of no img data
                                    
    if (img) == emp.itmLogo: 
        print("image didn't changed...............")
        pass
    else:
      try:
          print("image changed...............")
          os.remove(emp.itmLogo.path)
      except:
          pass

    itemExt.save()


    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'itmCode': Data['itmCode'],
              'itmName': Data['itmName'], 
              'opeQty': Data['opeQty'],
              'cloQty':0 , 
              'itmActive': Data['itmActive'],
              'itmLogo': '',
              'uPrice': Data['uPrice'],	
              'brand': Data['brand'],	
              'supplier': Data['supplier'],	
              'barCode': Data['barCode'],
              'uom': Data['uom'],
              'min': Data['min'],	
              'max': Data['max'],
              'roQty': Data['roQty'],
              'discount': Data['discount'],	
              'taxable': Data['taxable'],	
              'input': Data['input'],
              'output': Data['output'],
              'bisUnit': Data['bisUnit'],
              'itmType': Data['itmType'],
              'expiry': Data['expiry'],
              'ref': Data['ref'],
              'comment': '',
            }


    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/H1_Items/Item/ItemMaster.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



#☰☰☰ DELETE ITEMS ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delItm(request, pk):

  #----------Delete Record -----------------------------------------------
    ItmBasic = itmBasic.objects.get(id=pk)
    ItmExtra = itmExtra.objects.get(id=pk)

    if (ItmBasic.opeQty) == '':
        ItmBasic.opeQty = 0

    # if ther is any balance in either Opening and closing Item will not delete
    if (ItmBasic.opeQty) == 0 and ItmBasic.cloQty == 0:
      #----------Handle Image Deletion -------------------------------------
      if (ItmExtra.itmLogo) != "Blank.jpg":
          try:
              os.remove(ItmExtra.itmLogo.path)
          except:
              pass


      ItmBasic.delete()
      ItmExtra.delete()

      #Variable to Save in CSV File ..........
      tempDf = {'id': pk, 
              'itmCode': pk,
              'itmName': '', 
              'opeQty': '',
              'cloQty':'' , 
              'itmActive': '',
              'itmLogo': '',
              'uPrice': '',	
              'brand': '',	
              'supplier': '',	
              'barCode': '',
              'uom': '',
              'min': '',	
              'max': '',
              'roQty': '',
              'discount': '',	
              'taxable': '',	
              'input': '',
              'output': '',
              'bisUnit': '',
              'itmType': '',
              'expiry': '',
              'ref': '',
              'comment': 'Delete',
            }

      df = pd.DataFrame(tempDf, index=[0])
      df.to_csv('Data/H1_Items/Item/ItemMaster.csv',index=False, header=False, mode='a')
      
      return Response('Items delete successfully!')

    return Response('Unable to delet....!')



#☰☰☰ ITEMS SALES PRICE ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def itemPrice(request):
    #(Show the Detail Supplier Information)

    ###---- Read Employee master File ------------------------------------------
    df = pd.read_csv("Data/H1_Items/Item/ItemSalPrice.csv",encoding='unicode_escape').fillna(0)


    # remove duplicate rows and keep only the last occurrence subequently if that customer Code added
    DataA = df.drop_duplicates(subset=['itmCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 





#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Item Master Data ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def sItemLedger(request):
    #(Supplier Main Page)
    context = {'basData':'basData' }

    return render(request, 'H1_Items/sItemLedger.html', context)


def sItemLedgerURL(request, pk):
    pk = int(pk)
    

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/ItemMovement.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna(0)


    #pk = 1900
    df = df[df['itmCode'] == pk]
    df['traDat'] = pd.to_datetime(df['traDat']).dt.strftime('%Y-%m-%d')
    ledger = df
    ledger = ledger.sort_values('traDat')  # Sort by date in ascending order

    ### Remove Duplicate Quote and Deleted Record...
    ledger = ledger.drop_duplicates(subset=['id'], keep='last')
    ledger = ledger.drop(ledger.loc[ledger['action']=='Deleted'].index)

    ledger['totCost'] = ledger['costPU'] * ledger['qtyTOT']
    ledger['cumQty'] = ledger['qtyTOT'].cumsum()


  ### Step 2. to Calculate Horizontal - through iterrows ---------------------
  ### ========================================================================
    wac_list = []
    for index, row in ledger.iterrows():
        if row['Remarks'] == 'Balance':
            wac = row['costPU']
        elif row['Remarks'] == 'Purchase':
            wac = ((wac_list[-1] * (row['cumQty']-row['qtyTOT'])) + (row['totCost']))/ (row['cumQty'])
        elif row['Remarks'] == 'Sales':
            wac = (((wac_list[-1] * (row['cumQty']-row['qtyTOT'])) + (row['totCost'])) + (row['qtyTOT'] * wac_list[-1])) / (row['cumQty'])
        else:
            wac = 0
        wac_list.append(wac)

    ledger['WAC'] = wac_list


  ### Step 3. Change Transaction date format--- ------------------------------
  ### ========================================================================
    ledger['Balance'] = ledger['WAC']*ledger['cumQty']

    ledger.loc[ledger['Remarks'] == 'Sales', 'totCost'] = ledger.loc[ledger['Remarks'] == 'Sales', 'qtyTOT'] * ledger.loc[ledger['Remarks'] == 'Sales', 'WAC']
    ledger['costPU'] = ledger['totCost'] / ledger['qtyTOT']

    ledgerA = ledger[['itmCode','itmName','traDat','desc','costPU','qtyTOT','totCost','cumQty','WAC','Balance']]

    Data = ledgerA.to_dict(orient="records")

    return JsonResponse(Data, safe=False) 




#☰☰☰ UPLOAD ITEMS MASTER DATA ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def zUploadItmData(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_itmBasic = request.FILES['myfile']

        if not new_itmBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_itmBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              value = itmBasic(data [0], data [1], data [2], data [3], data [4], data [5],)
              value.save()

              value2 = itmExtra(data [0], data [1], data [6], data [7], data [8], data [9],data [10],
                                data [11], data [12], data [13], data [14],data [15], data [16],
                                data [17], data [18], data [19], data [20],data [21],data [22],)
              value2.save()
            
        messages.info(request,'Upload Successfully')

    return render(request, 'H1_Items/zUploadItmData.html')



def zUploadItmLedger(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_itmBasic = request.FILES['myfile']

        if not new_itmBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_itmBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              
              value = itmLedger(data [0], data [1], data [2], data [3], data [4], data [5], data [6], data [7], data [8], data [9], )
              value.save()

            
        messages.info(request,'Upload Successfully')

    return render(request, 'H1_Items/zUploadItmLedger.html')

