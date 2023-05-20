from django.shortcuts import render, redirect, HttpResponse
import os


from G1_Purchases.models import supBasic, supExtra

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
from .resources import supBasicResource, supExtraResource
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload



### Data Base and Serializers ----------------------------
from G1_Purchases.serializers import supBasicSerializer, supExtraSerializer, supInitSerializer



import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')



# from django.template import RequestContext

#☰☰☰ SALES Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aPurchasesModule(request):
    context = {'abc':'abc', }
    return render(request, 'G1_Purchases/aPurchasesModule.html', context)



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Supplier Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aSupplierList(request):
    #(Supplier Main Page)
    context = {'basData':'basData' }
    return render(request, 'G1_Purchases/aSupplierList.html', context)


def aSupRefresh(request):

  ### Step 1 - Read Data from SQL--------------------------------------------
  ### =======================================================================
    basic = pd.read_sql('''SELECT * FROM "G1_Purchases_supBasic" ''', con=engine)
    Extra = pd.read_sql('''SELECT * FROM "G1_Purchases_supExtra" ''', con=engine)


  ### Step 2 - Merge "Basic & Extra" Dataframe by Supplier ID----------------
  ### =======================================================================
    Combined = pd.merge(basic, Extra, on=["supCode"])
    Combined = Combined.drop("id_y", axis=1)
    Combined = Combined.rename(columns={'id_x': 'id'})

    Combined['comment'] = ''


  ### Step Step 3 - Create a "Supplier" Folder inside "Data/G1_Purchases" Folder-
  ### =======================================================================
    data_folder = "Data/G1_Purchases"
    purchases_folder = "Supplier"

    if not os.path.exists(os.path.join(data_folder, purchases_folder)):
        os.makedirs(os.path.join(data_folder, purchases_folder))
    else:
        pass


  ### Step 4 - Save Supplier Master File as CSV File ------------------------
  ### =======================================================================
    #https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
    Combined.to_csv('Data/G1_Purchases/Supplier/SuppMaster.csv',index = False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def showSupp(request):
    #(Show the Detail Supplier Information)

    ### Read CSV Files in Pandas...........................
    df = pd.read_csv("Data/G1_Purchases/Supplier/SuppMaster.csv").fillna(0)

    # remove duplicate rows and keep only the last occurrence
    DataA = df.drop_duplicates(subset=['supCode'], keep='last')
    # remove rows where comment column have string 'Delele'
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ### Convert Data into Json Dictionary..................
    Data = DataB.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def supBasInfo(request):
    #(Get Specific column from Customer Basic DataTable)

    Detail = supBasic.objects.only('id', 'supCode', 'supName') 
    serilizer = supInitSerializer(Detail, many=True)
    return Response(serilizer.data)


def addSupplier(request):
    #(Screen to Add New Cutomer)
    context = {'Data':'Data' }
    return render(request, 'G1_Purchases/addSupplier.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def addSupp(request):
    Data = request.data
    
    #---- Supplier Basic Information ---------------------------------------
    supplierBasic = supBasic (Data['id'], Data['supCode'],Data['supName'],
                              Data['opeBal'], 0 , Data['supActive'],)
    supplierBasic.save()

    #---- Supplier Extra Information ---------------------------------------
    supplierExt = supExtra (  Data['id'], Data['supCode'], Data['supLogo'], Data['supPhone'], 
                              Data['supEmail'], Data['supWeb'], Data['supBillFrom'], 
                              Data['supShipFrom'], Data['supAcNum'], Data['supCrLim'], 
                              Data['supPytTerm'], Data['supBank'], Data['supLegName'], 
                              Data['supTRN'], Data['supTP'], Data['supTOJ'], 
                              Data['supCP'], Data['supCPN'],
                            )
    supplierExt.save()

    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'supCode': Data['supCode'],
              'supName': Data['supName'], 
              'opeBal': Data['opeBal'],
              'cloBal':0 , 
              'supActive': Data['supActive'],
              'supLogo': '',
              'supPhone': Data['supPhone'],	
              'supEmail': Data['supEmail'],	
              'supWeb': Data['supWeb'],	
              'supBillFrom': Data['supBillFrom'],
              'supShipFrom': Data['supShipFrom'],
              'supAcNum': Data['supAcNum'],	
              'supCrLim': Data['supCrLim'],
              'supPytTerm': Data['supPytTerm'],
              'supBank': Data['supBank'],	
              'supLegName': Data['supLegName'],	
              'supTRN': Data['supTRN'],
              'supTP': Data['supTP'],
              'supTOJ': Data['supTOJ'],
              'supCP': Data['supCP'],
              'supCPN': Data['supCPN'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/G1_Purchases/Supplier/SuppMaster.csv',index=False, header=False, mode='a')
    #df.to_csv('Data/G1_Purchases/Customer/tempCust.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def aEditSupplier(request, pk):

    SupBasic = supBasic.objects.get(id=pk)
    SupExtra = supExtra.objects.get(id=pk)
    #print(SupBasic.supCode)

    serBasic = supBasicSerializer(SupBasic, many=False)
    serExtra = supExtraSerializer(SupExtra, many=False)
    #print(serExtra.data)

    ser_Basic = {k: '' if v is None else v for k, v in serBasic.data.items()}
    ser_Extra = {k: '' if v is None else v for k, v in serExtra.data.items()}

    #(Screen to Add New Supplier)
    context = {'DataA':ser_Basic, 'DataB':ser_Extra,}
    return render(request, 'G1_Purchases/aEditSupplier.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def editSup(request):
    
    Data = request.data
    emp = supExtra.objects.get(id=Data['id'])
    #print(Data)
    
    #---- Supplier Basic Information ---------------------------------------
    supplierBasic = supBasic (Data['id'], Data['supCode'],Data['supName'],
                              Data['opeBal'], 0 , Data['supActive'],)
    supplierBasic.save()


    #---- Supplier Extra Information ---------------------------------------
    supplierExt = supExtra (  Data['id'], Data['supCode'], Data['supLogo'], Data['supPhone'], 
                              Data['supEmail'], Data['supWeb'], Data['supBillFrom'], 
                              Data['supShipFrom'], Data['supAcNum'], Data['supCrLim'], 
                              Data['supPytTerm'], Data['supBank'], Data['supLegName'], 
                              Data['supTRN'], Data['supTP'], Data['supTOJ'], 
                              Data['supCP'], Data['supCPN'],
                          )


    img = Data['supLogo'] #will return sting incase of no img data
                                    
    if (img) == emp.supLogo: 
        print("image didn't changed...............")
        pass
    else:
      try:
          print("image changed...............")
          os.remove(emp.supLogo.path)
      except:
          pass

    supplierExt.save()


    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'supCode': Data['supCode'],
              'supName': Data['supName'], 
              'opeBal': Data['opeBal'],
              'cloBal':0 , 
              'supActive': Data['supActive'],
              'supLogo': '',
              'supPhone': Data['supPhone'],	
              'supEmail': Data['supEmail'],	
              'supWeb': Data['supWeb'],	
              'supBillFrom': Data['supBillFrom'],
              'supShipFrom': Data['supShipFrom'],
              'supAcNum': Data['supAcNum'],	
              'supCrLim': Data['supCrLim'],
              'supPytTerm': Data['supPytTerm'],
              'supBank': Data['supBank'],	
              'supLegName': Data['supLegName'],	
              'supTRN': Data['supTRN'],
              'supTP': Data['supTP'],
              'supTOJ': Data['supTOJ'],
              'supCP': Data['supCP'],
              'supCPN': Data['supCPN'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/G1_Purchases/Supplier/SuppMaster.csv',index=False, header=False, mode='a')
    

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delSup(request, pk):

  #----------Delete Record -----------------------------------------------
    SupBasic = supBasic.objects.get(id=pk)
    SupExtra = supExtra.objects.get(id=pk)

    if (SupBasic.opeBal) == '':
        SupBasic.opeBal = 0

    # if ther is any balance in either Opening and closing supplier will not delete
    if (SupBasic.opeBal) == 0 and SupBasic.cloBal == 0:
      #----------Handle Image Deletion -------------------------------------
      if (SupExtra.supLogo) != "Blank.jpg":
          try:
              os.remove(SupExtra.supLogo.path)
          except:
              pass


      SupBasic.delete()
      SupExtra.delete()

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
                'cusBillFrom': '',
                'cusShipFrom': '',
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
      df.to_csv('Data/G1_Purchases/Supplier/SuppMaster.csv',index=False, header=False, mode='a')
      
      return Response('Items delete successfully!')

    return Response('Unable to delet....!')




def zUploadSupData(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_supBasic = request.FILES['myfile']

        if not new_supBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_supBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              value = supBasic(data [0], data [1], data [2], data [3], data [4], data [5],)
              value.save()

              value2 = supExtra(data [0], data [1], data [6], data [7], data [8], data [9],data [10],
                                data [11], data [12], data [13], data [14],data [15], data [16],
                                data [17], data [18], data [19], data [20],data [21],)
              value2.save()
            
        messages.info(request,'Upload Successfully')

    return render(request, 'G1_Purchases/zUploadSupData.html')


