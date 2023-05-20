from django.shortcuts import render, redirect, HttpResponse
import os
import csv

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




#☰☰☰ SALES Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aEmployeeModule(request):
    context = {'abc':'abc', }
    return render(request, 'I1_HRM/aEmployeeModule.html', context)




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Employee Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aEmployeeList(request):
    #(Employee Main Page)
    context = {'basData':'basData' }
    return render(request, 'I1_Hrm/aEmployeeList.html', context)


def aEmpRefresh(request):

  ### Step 1 - Read Data from SQL--------------------------------------------
  ### =======================================================================
    basic = pd.read_sql('''SELECT * FROM "I1_Hrm_empBasic" ''', con=engine)
    Extra = pd.read_sql('''SELECT * FROM "I1_Hrm_empExtra" ''', con=engine)

  ### Step 2 - Merge "Basic & Extra" Dataframe by Supplier ID----------------
  ### =======================================================================
    Combined = pd.merge(basic, Extra, on=["empCode"])
    Combined = Combined.drop("id_y", axis=1)
    Combined = Combined.rename(columns={'id_x': 'id'})

    arrColumn= ['id','empCode','empFName','empMName','empLName','empStat','empImg','empPosi',
                'empDoj','empEid','empLoca','empDept','empRepTo','empSpon','empNatl','empGend',
                'empDob','EmpMarr','empIban','empBank','empAcc','empUid','empVisa','empAdd','empPh','empEmail','ref'
              ]
    Combined = Combined.reindex(columns=arrColumn)

    Combined['comment'] = ''


  ### Step Step 3 - Create a "Supplier" Folder inside "Data/G1_Purchases" Folder-
  ### =======================================================================
    data_folder = "Data/I1_Hrm"
    sales_folder = "Employees"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass


  ### Step 4 - Save Employee Master File as CSV File ------------------------
  ### =======================================================================
    #https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
    Combined.to_csv('Data/I1_Hrm/Employees/EmpMaster.csv',index = False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def showEmp(request):
    #(Show the Detail Supplier Information)

    ### Step 1 - Read CSV files - Through Pandas and get the list of a column-------------
    ###------------------------------------------------------------------------------------
    df = pd.read_csv("Data/I1_Hrm/Employees/EmpMaster.csv",encoding='unicode_escape').fillna('')


   ### Step 2 - Remove duplicate rows and keep only the last occurrence -----------------
   ###-----------------------------------------------------------------------------------
    DataA = df.drop_duplicates(subset=['empCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)


   ### Step 3 - Convert Data into Json Dictionary (can be access by JavaScript) --------
    Data = DataB.to_dict(orient="records")


    ### Return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 


def addEmployee(request):
    #(Screen to Add New Cutomer)
    context = {'Data':'Data' }
    return render(request, 'I1_Hrm/addEmployee.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def addEmpl(request):
    Data = request.data
    
    #---- Employee Basic Information ---------------------------------------
    employeeBasic = empBasic (Data['id'], Data['empCode'],Data['empFName'],
                              Data['empMName'], Data['empLName'] , Data['empStat'],)
    employeeBasic.save()

    #---- Employee Extra Information ---------------------------------------
    employeeExt = empExtra (  Data['id'], Data['empCode'], Data['empImg'], Data['empPosi'], 
                              Data['empDoj'], Data['empEid'], Data['empLoca'], 
                              Data['empDept'], Data['empRepTo'], Data['empSpon'], 
                              Data['empNatl'], Data['empGend'], Data['empDob'], 
                              Data['EmpMarr'], Data['empIban'], Data['empBank'], 
                              Data['empAcc'], Data['empUid'],Data['empVisa'], Data['empAdd'],
                              Data['empPh'], Data['empEmail'],Data['ref'],
                            )
    employeeExt.save()

    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'empCode': Data['empCode'],
              'empFName': Data['empFName'], 
              'empMName': Data['empMName'],
              'empLName': Data['empLName'] , 
              'empStat': Data['empStat'],
              'empImg': '',
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
              'EmpMarr': Data['EmpMarr'],
              'empIban': Data['empIban'],
              'empBank': Data['empBank'],
              'empAcc': Data['empAcc'],
              'empUid': Data['empUid'],
              'empVisa': Data['empVisa'],
              'empAdd': Data['empAdd'],
              'empPh': Data['empPh'],
              'empEmail': Data['empEmail'],
              'ref': Data['ref'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/I1_Hrm/Employees/EmpMaster.csv',index=False, header=False, mode='a')


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def empBasInfo(request):
    #(Get Specific column from Customer Basic DataTable)

    Detail = empBasic.objects.only('id', 'empCode', 'empFName') 
    serilizer = empInitSerializer(Detail, many=True)
    return Response(serilizer.data)



@api_view(['GET'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def editEmployee(request, pk):

    EmpBasic = empBasic.objects.get(id=pk)
    EmpExtra = empExtra.objects.get(id=pk)
    #print(CusBasic.cusCode)

    serBasic = empBasicSerializer(EmpBasic, many=False)
    serExtra = empExtraSerializer(EmpExtra, many=False)
    #print(serExtra.data)

    #to use serializer in Javascript without any further process.........................
    #creates a new dictionary with the same keys as the "serializer.data" dictionary, but with any None values replaced by empty strings.
    ser_Basic = {k: '' if v is None else v for k, v in serBasic.data.items()}
    ser_Extra = {k: '' if v is None else v for k, v in serExtra.data.items()}

    #(Screen to Add New Cutomer)
    context = {'DataA':ser_Basic, 'DataB':ser_Extra,}
    return render(request, 'I1_Hrm/editEmployee.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def editEmp(request):
    
    Data = request.data
    emp = empExtra.objects.get(id=Data['id'])
    #print(Data)
    
    #---- Customer Basic Information ---------------------------------------
    employeeBasic = empBasic (Data['id'], Data['empCode'],Data['empFName'],
                              Data['empMName'], Data['empLName'] , Data['empStat'],)
    employeeBasic.save()



    #---- Customer Extra Information ---------------------------------------
    employeeExt = empExtra (  Data['id'], Data['empCode'], Data['empImg'], Data['empPosi'], 
                              Data['empDoj'], Data['empEid'], Data['empLoca'], 
                              Data['empDept'], Data['empRepTo'], Data['empSpon'], 
                              Data['empNatl'], Data['empGend'], Data['empDob'], 
                              Data['EmpMarr'], Data['empIban'], Data['empBank'], 
                              Data['empAcc'], Data['empUid'],Data['empVisa'], Data['empAdd'],
                              Data['empPh'], Data['empEmail'],Data['ref'],
                            )

    img = Data['empImg'] #will return sting incase of no img data
                                    
    if (img) == emp.empImg: 
        print("image didn't changed...............")
        pass
    else:
      try:
          print("image changed...............")
          os.remove(emp.empImg.path)
      except:
          pass

    employeeExt.save()


    #Variable to Save in CSV File ..........
    tempDf = {'id': Data['id'], 
              'empCode': Data['empCode'],
              'empFName': Data['empFName'], 
              'empMName': Data['empMName'],
              'empLName': Data['empLName'] , 
              'empStat': Data['empStat'],
              'empImg': '',
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
              'EmpMarr': Data['EmpMarr'],
              'empIban': Data['empIban'],
              'empBank': Data['empBank'],
              'empAcc': Data['empAcc'],
              'empUid': Data['empUid'],
              'empVisa': Data['empVisa'],
              'empAdd': Data['empAdd'],
              'empPh': Data['empPh'],
              'empEmail': Data['empEmail'],
              'ref': Data['ref'],
              'comment': '',
            }

    df = pd.DataFrame(tempDf, index=[0])
    df.to_csv('Data/I1_Hrm/Employees/EmpMaster.csv',index=False, header=False, mode='a')
    #df.to_csv('Data/F1_Sales/Customer/tempCust.csv',index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)



@api_view(['DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def delEmp(request, pk):
  #----------Delete Record -----------------------------------------------
    EmpBasic = empBasic.objects.get(id=pk)
    EmpExtra = empExtra.objects.get(id=pk)

    # if ther is any balance in either Opening and closing Item will not delete
    if (EmpBasic.empStat) == 'Inactive': 
      
      #----------Handle Image Deletion -------------------------------------
      if (EmpExtra.empImg) != "Blank.jpg":
          try:
              os.remove(EmpExtra.empImg.path)
              print("================================")
              print(EmpBasic.empStat)
          except:
              pass

      EmpBasic.delete()
      EmpExtra.delete()

      #Variable to Save in CSV File ..........
      tempDf = {'id': pk, 
              'empCode': pk,
              'empFName': '', 
              'empMName': '',
              'empLName': '' , 
              'empStat': '',
              'empImg': '',
              'empPosi': '',	
              'empDoj': '',	
              'empEid': '',	
              'empLoca': '',
              'empDept': '',
              'empRepTo': '',	
              'empSpon': '',
              'empNatl': '',
              'empGend': '',	
              'empDob': '',	
              'EmpMarr': '',
              'empIban': '',
              'empBank': '',
              'empAcc': '',
              'empUid': '',
              'empVisa': '',
              'empAdd': '',
              'empPh': '',
              'empEmail': '',
              'ref': '',
              'comment': 'Delete',
            } 

      df = pd.DataFrame(tempDf, index=[0])
      df.to_csv('Data/I1_Hrm/Employees/EmpMaster.csv',index=False, header=False, mode='a')
      
      return Response('Items delete successfully!')

    return Response('Unable to delet....!')




#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Employee Target ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def tEmpTarget(request):
    #(To Set Employee Sales Target)

    ### Step 1 - Read CSV files - Through Pandas and get the list of a column
    ### ---------------------------------------------------------------------
    try: #incase there is no folder and files to avoid error
      filename = "Data/2023/I1_Hrm/Employees/empTarget.csv"
      df = pd.read_csv(filename, index_col=False).fillna(0)
    except:
        data = {'empCode': ['John', 'Alice', 'Doe'],
                'comment': ['A','B','C']}
        df = pd.DataFrame(data)

    ### Step 1a - Remove Duplicate Line and Deleted Record ------------------
    DataA = df.drop_duplicates(subset=['empCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ### Step 1b - Select a Column and Convert into List ---------------------
    List = DataB["empCode"].tolist()

    context = {'List':List }
    return render(request, 'I1_Hrm/tEmpTarget.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def tEmpTargetURL(request):
    #(To Save detail Sales Target)

    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])    

    Data = request.data[0]
    addiData = request.data
    #print(request.data)

    ### Create Folder If not Already Exist.............................
    data_folder = 'Data/'+Year+'/I1_Hrm'
    sales_folder = "Employees"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass

    file_path = 'Data/'+Year+'/I1_Hrm/Employees/empTargetDetail.csv'
    if os.path.isfile(file_path):
      pass
    else:
      req_cols = ['id','empCode','empName','anSalary','anTarget','sno','itmcode','desc','itemselprice','qty','salestarget','totalsalcost','salcostpu','traDate','comment']
      df = pd.DataFrame(columns=req_cols)
      df.to_csv('Data/'+Year+'/I1_Hrm/Employees/empTargetDetail.csv', index=False, mode='a')


    for Data in addiData:
        #Variable to Save in CSV File ..........
        tempDf = { 'id':	Data['empCode'],
                  'empCode':	Data['empCode'], 
                  'empName':	Data['empName'], 
                  'anSalary':	Data['anSalary'], 
                  'anTarget':	Data['anTarget'], 
                  'sno':	Data['sno'],
                  'itmcode':	Data['itmcode'],
                  'desc':	Data['itmdesc'],
                  'itemselprice': Data['itemselprice'],
                  'qty':	Data['qty'],
                  'salestarget':	Data['salestarget'],
                  'totalsalcost':	Data['totalsalcost'],
                  'salcostpu':	Data['salcostpu'],
                  'traDate':	Data['traDate'],   
                  'comment':	'', 
                }
        df = pd.DataFrame(tempDf, index=[0])
        df.to_csv('Data/'+Year+'/I1_Hrm/Employees/empTargetDetail.csv',index=False, header=False, mode='a')

    updateDf = {
              'id': Data['empCode'],
              'empCode':	Data['empCode'], 
              'empName':	Data['empName'], 
              'empImg': Data['image'],
              'empPosi': Data['empPosi'],
              'anSalary':	Data['anSalary'], 
              'anTarget':	Data['anTarget'],
              'empStat': 'Active',
              'targetSet': 'Yes',
              'traDate':Data['traDate'], 
              'comment':	'',   
            }
    
    df2 = pd.DataFrame(updateDf, index=[0])
    df2.to_csv('Data/'+Year+'/I1_Hrm/Employees/empTarget.csv',index=False, header=False, mode='a')

    jsonData = {"Refere":'metRef' }
    return JsonResponse(jsonData)



def tEmpTargetEdit(request):
    #(To Set Employee Sales Target)

  ##----DEFAULT INFORMATION--------------------------------------------------
    dfA = pd.read_csv('data/basInfo.csv')
    Year = str(dfA.loc[0, 'year'])    
  ##----DEFAULT INFORMATION--------------------------------------------------


  ### Step 1 - Read CSV files - Through Pandas and get the list of a column
  ### ---------------------------------------------------------------------
    Year = '2023'
    try: #incase there is no folder and files to avoid error
        req_cols = ['empCode','anSalary', 'anTarget','empStat','targetSet','comment']
        dfSel = pd.read_csv("Data/"+Year+"/I1_Hrm/Employees/empTarget.csv", usecols=req_cols, index_col=False).fillna(0)
        reqB = ['empCode','empFName', 'empMName','empLName','empImg','empPosi','comment']
        dfDetail = pd.read_csv("Data/I1_Hrm/Employees/EmpMaster.csv", usecols=reqB, index_col=False)
    except:
        data = {'empCode': ['John', 'Alice', 'Doe'], 'comment': ['A','B','C']}
        df = pd.DataFrame(data)

    ### Step 1a- Step 1a- Remove Duplicate Line and Deleted Record ----------
    dfSel = dfSel.drop_duplicates(subset=['empCode'], keep='last')
    dfSel = dfSel.drop(dfSel.loc[dfSel['comment']=='Delete'].index)

    ### Step 1a- Step 1a- Remove Duplicate Line and Deleted from master ----------
    dfDetail = dfDetail.drop_duplicates(subset=['empCode'], keep='last')
    dfDetail= dfDetail.drop(dfDetail.loc[dfDetail['comment']=='Delete'].index)

    ### Step 1b- Updated with Master File -----------------------------------
    dfDetail = dfDetail.fillna('')
    dfDetail['empName'] = dfDetail['empFName']+" "+dfDetail['empMName']+" "+dfDetail['empLName']
    DataB= pd.merge(dfSel, dfDetail, on ='empCode', how ='inner')


    ### Step 1c- Get Selected Columns --------------------------------------
    iniData = DataB[['empCode','empName','empPosi','anTarget', 'empImg', 'anSalary']]



  ### Step 1 - Convertion the Data - into Dictionary ----------------------
  ### ---------------------------------------------------------------------
    Data=[]
    for i in range(iniData.shape[0]):
            temp=iniData.iloc[i]
            Data.append(dict(temp))

    context = {'Data':Data }
    return render(request, 'I1_Hrm/tEmpTargetEdit.html', context)



@api_view(['Get'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def tEmpTargetFetchURL(request, pk):
    iID = pk

  ##--Step 1 - Read empTarget - Through Pandas and get the list of a column
  ##----------------------------------------------------------------------------
    df = pd.read_csv("Data/2023/I1_Hrm/Employees/empTarget.csv", index_col=False ,encoding='unicode_escape').fillna(0)

    ##--Step 1a - Remove Duplicate Line and Deleted Record ---------------------
    DataA = df.drop_duplicates(subset=['empCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ##--Step 1b - Combine Employee Code and Transaction Time -------------------
    DataB['combined'] = DataB['empCode'].astype(str)+" "+DataB['traDate']

    ##--Step 1c- Select the Combine Column and convert it into a "LIST" --------
    List = DataB["combined"] #.tolist()


  ##--Step 2 - Read empTarget - Through Pandas and get the list of a column
  ##----------------------------------------------------------------------------
    Year = '2023'
    df2 = pd.read_csv("Data/"+Year+"/I1_Hrm/Employees/empTargetDetail.csv", index_col=False).fillna(0)
    ### Combine Employee Code and Transaction Time.................
    df2['combined'] = df2['empCode'].astype(str)+" "+df2['traDate']

    ##--Step 2a- Filtere the 'Employee Target Detail' by Employee "Target List"---
    filtered_df = df2[df2['combined'].isin(List)]
    #Convert 'salesTarget' astype to "FLOAT" to avoid error if any numaric value contain float type.
    filtered_df = filtered_df.astype({'salesTarget':'float'})

    ID = int(iID)
    seleData = filtered_df[filtered_df['empCode'] == ID]
    result_jsRecord = seleData.to_dict(orient="records")   

    jsonData = {"Refere":result_jsRecord}
    return JsonResponse(jsonData)



#☰☰☰ EMPLOYEE SALARY DETAIL ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def empSalary(request):
    #(Show the Detail Supplier Information)


    ###---- Step 1b - Read Data from SQL ---------------------------------------
    basic = pd.read_sql('''SELECT * FROM "I1_Hrm_empBasic" ''', con=engine)
    Extra = pd.read_sql('''SELECT * FROM "I1_Hrm_empExtra" ''', con=engine)


  ### Step 2 - Merge "Basic & Extra" Dataframe by Customer ID -----------
    Combined = pd.merge(basic, Extra, on=["empCode"])
    Combined = Combined.drop("id_y", axis=1)
    Combined = Combined.rename(columns={'id_x': 'id'})

    Combined = Combined.fillna('')
    Combined['empName'] = Combined['empFName']+" "+Combined['empMName']+" "+Combined['empLName'] 

    DataB = Combined.loc[:, ['empCode', 'empName', 'empImg', 'empPosi', 'empStat']].fillna(0) 

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = DataB.to_dict(orient="records")

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

