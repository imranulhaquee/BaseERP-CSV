from django.shortcuts import render, redirect, HttpResponse
import os

from C1_Gl.models import triBal

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
from .resources import triBalResource
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload

### Data Base and Serializers ----------------------------
from C1_Gl.serializers import triBalSerializer

### --- Get Data from DataBse through Pands --------------
import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')


### --- Generate PDF ------------------------------------
from django.template.loader import get_template
from xhtml2pdf import pisa 

# Create your views here.

#☰☰☰ GL Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aGlModule(request):
    context = {'abc':'abc', }
    return render(request, 'C1_Gl/aGlModule.html', context)


def CoA(request):

    ###---- Step 1 - Read Excel files ------------------------------------------
    df = pd.read_excel("Data/B1_Setup/CoA/CoA Level.xlsx").fillna(0)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = df.values.tolist()

    context = {'Data':Data, }
    return render(request, 'C1_Gl/CoA.html', context)



def aTrialBalance(request):
    #(Employee Main Page)
    context = {'basData':'basData' }
    return render(request, 'C1_Gl/aTrialBalance.html', context)


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
    data_folder = "Data/I1_Employees"
    sales_folder = "Employees"

    if not os.path.exists(os.path.join(data_folder, sales_folder)):
        os.makedirs(os.path.join(data_folder, sales_folder))
    else:
        pass


  ### Step 4 - Save Supplier Master File as CSV File ------------------------
  ### =======================================================================
    #https://sparkbyexamples.com/pandas/pandas-write-dataframe-to-csv-file/
    Combined.to_csv('Data/I1_Employees/Employees/EmpMaster.csv',index = False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def showTb(request):
    #(Show the Detail Supplier Information)

    ###---- Read Employee master File ------------------------------------------
    df = pd.read_csv("Data/C1_Gl/Tb/Tb.csv",encoding='unicode_escape').fillna('')


    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = df.to_dict(orient="records")

    ### return Response data in List form i.e. [Data, page, id] we can send without [ ]
    return JsonResponse(Data, safe=False) 




def CoAEdit(request, pk):

    Account = triBal.objects.get(id=pk)
    #print(SupBasic.supCode)

    serBasic = triBalSerializer(Account, many=False)
    #print(serExtra.data)

    ser_Basic = {k: '' if v is None else v for k, v in serBasic.data.items()}


    ###---- Step 1 - Read Excel files ------------------------------------------
    df = pd.read_excel("Data/B1_Setup/CoA/CoA Level.xlsx").fillna(0)

    ### Convert Data into Json Dictionary (can be access by JavaScript) .........
    Data = df.values.tolist()

    #(Screen to Add New Supplier)
    context = {'DataA':ser_Basic, 'Data':Data}
    return render(request, 'C1_Gl/CoAEdit.html', context)



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Journal Ledger ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def TrialBalance(request):
    

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Read Journals.csv to get the transaction detail ------------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    transaction = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna(0)

    ### file doesn't recongnize date formate first convert into date and than strftime
    transaction['Date'] = pd.to_datetime(transaction['Date']).dt.strftime('%Y-%m-%d')
    transaction = transaction.sort_values(['Date'], ascending = [True])


    ### Read mergeTB.csv to get to merge transactio with mergeTB...................
    fPath = "Data/" +coFolder+ "/C1_Gl/mergeTB.csv"
    mergeTB = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna(0)


  ### Step 3 - Create Pivot Table - to Create TB -----------------------------
  ### ========================================================================
    pTransaction = pd.pivot_table(transaction,index=["accCode","accHead"],values=["Amount"],aggfunc=[np.sum],fill_value=0)

    pTransaction.columns = pTransaction.columns.droplevel(0)
    pTransaction.reset_index(inplace=True)


  ### Step 4 - Merge pTransaction with mergeTB- to Create TB -----------------
  ### ========================================================================
    merged_df = pTransaction.merge(mergeTB[['head', 'level1', 'level2', 'level3', 'level4']], left_on='accHead', right_on='head', how='left')
    merged_df = merged_df.drop('head', axis=1).fillna('')  # Drop the 'head' column from the merged DataFrame


  ### Step 5 - Create Pivot Table - to Create TB -----------------------------
  ### ========================================================================
    final = pd.pivot_table(merged_df,index=["level4","accHead","accCode"],values=["Amount"],aggfunc=[np.sum],fill_value=0)

    final.columns = final.columns.droplevel(0)
    final.reset_index(inplace=True)

    finalGBy = final.groupby(['level4']).agg({'Amount': 'sum'}) 
    finalGBy.loc['z. Grand Total'] = finalGBy.sum()
    finalGBy.reset_index(inplace=True)

    tbConcat = pd.concat([final, finalGBy])

    tbSort = tbConcat.sort_values(['level4','accHead'], ascending = [True,True], na_position ='last')
    tbSort['accHead'] = tbSort['accHead'].fillna('Total')

    ### to Hide and Show----------------------------
    tbSort['Department'] = tbSort['level4']
    tbSort['Vertical'] = tbSort['level4']
    tbSort.loc[tbSort["accHead"] != "Total", ["Vertical"]] = '---' #  rlSort["status"]    tbSort = tbSort.fillna('')
    tbSort = tbSort.fillna('')


    Data = tbSort.to_dict(orient="records")


    #(Supplier Main Page)
    context = {'Data':Data }

    return render(request, 'C1_Gl/TrialBalance.html', context)



def syncGenLeger(request): #URL to fetch data--

  ### Get Company and Year - to Load Data ------------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read Journals.csv - to Refresh the data -----------------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna(0)

    ### create a unique Column to Merge Id and Item Code........
    df['unique'] = df['Ref'].astype(str)+ '-' +df['Type'].astype(str)+ '-' +df['accCode'].astype(str)

    ### Remove Duplicate Quote and Deleted Record...
    ledger = df.drop_duplicates(subset=['unique'], keep='last')
    ledger = ledger.drop(ledger.loc[ledger['action']=='Deleted'].index)

    ledger = ledger.drop('unique', axis=1)

    ### Save the data in qotBasic.csv File...
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    ledger.to_csv(fPath, index=False)


    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)


def sLedger(request, pk):
    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read dlBasic.csv - to Get the last Delivery Number ------------
  ### ========================================================================
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna(0)   

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df = df.sort_values(['Date'], ascending = [True])

    dfA  = df[df['accCode'] == pk].fillna(0) ### Filter data as per 'pk' selected quote

    ledgerA = dfA[['Date','accCode','accHead','Ref','Type','Amount','Comm']]
    ledgerB = ledgerA.copy()
    ledgerB['Balance'] = ledgerB['Amount'].cumsum()
    
    Data = ledgerB.to_dict(orient="records")

    print(Data)

    #(Supplier Main Page)
    context = {'Data':Data }

    return render(request, 'C1_Gl/sLedger.html', context)





#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Upload Trial Balance ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def zUploadTbData(request):
    
    if request.method == 'POST':
        dataset = Dataset()
        new_itmBasic = request.FILES['myfile']

        if not new_itmBasic.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_itmBasic.read(),format='xlsx')

        with transaction.atomic():
          for data in imported_data:
              value = triBal(data [0], data [1], data [2], data [3], data [4], data [5],
                             data [6], data [7], data [8], data [9], data [10],)
              value.save()
            
        messages.info(request,'Upload Successfully')

    return render(request, 'C1_Gl/zUploadTbData.html')





#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ EXPENSE RECORD ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰


def dJournalList(request):
    #(To Show all the Sales Order Basic Information Screen)
    context = {'Data':'Data' }
    return render(request, 'C1_Gl/dJournalList.html', context)


def dJournalListURL(request):
    #(Get All the Sales Delivery Detail)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read siBasic.csv File -----------------------------------------
  ### ========================================================================
    req_cols = ['Ref','Type','Date','Comm', 'traDate', 'action']
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    ### Filter the data by type ie 'ji'-------------------------
    df = df[df['Type'] == 'jl']

    df['unique'] =  df['Ref'].astype(str)+" "+df['traDate']

    ### Remove Duplicate Quote and Deleted Record...
    df = df.drop_duplicates(subset=['unique'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index)

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')


  ### Step 3. Convert Data into Dictionary -----------------------------------
  ### ========================================================================
    Data = df.to_dict(orient="records")


    return JsonResponse(Data, safe=False) 



def dJournalAdd(request):

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read journals.csv - to Get the last Journal Number ------------
  ### ========================================================================
    req_cols = ['Ref', 'Type']
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    df = pd.read_csv(fPath, usecols=req_cols, index_col=False, encoding='unicode_escape')

    ### Filter the data by type ie 'ji'-------------------------
    filtered_df = df[df['Type'] == 'jl']

    # Check if the DataFrame is empty max_value = 2300001 else get the max_value----------
    if filtered_df.empty:
        max_value = 2300000
    else:
        max_value = filtered_df['Ref'].max()


  ### Step 2 - Read DropDown.csv - to Get the list of Countries and Departments etc--
  ### ===============================================================================
    fPath = "Data/" +coFolder+ "/C1_Gl/DropDown/DropDown.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    Country = df[df['Type'] == 'Country']
    countryList = Country['Description'].tolist()

    Department = df[df['Type'] == 'Department']
    departmentList = Department['Description'].tolist()

    Brand = df[df['Type'] == 'Brand']
    brandList = Brand['Description'].tolist()

    context = {'lastJL':max_value, 'countryList':countryList, 'departmentList':departmentList, 'brandList':brandList}
    return render(request, 'C1_Gl/dJournalAdd.html', context)


@api_view(['POST'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def dJournalAddUrl(request):
    print(request.data)


  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Save Data in soStat.csv file ----------------------------------
  ### ========================================================================
    addiData = request.data
    addRecords = []
    for data in addiData:
      Amount =  int(data['debit']) - int(data['credit'])
          
      Addi  = { 'ref': data['jlRef'],
                'Type': 'jl',
                'Date':  data['jlDat'],
                'accCode':  data['accode'],
                'accHead':  data['achead'],
                'Amount' : Amount,
                'Cumm': data['jlDesc'],
                'traDate':data['traDate'],
                'action':" " ,   
                'brand': data['brand'],
                'department': data['department'],
                'country': data['country'],              
        }
      addRecords.append(Addi)  # Add the dictionary to the list

    dfAddi = pd.DataFrame(addRecords)
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    dfAddi.to_csv(fPath, index=False, header=False, mode='a')

    jsonData = {"name": "John", "age": 30,"address": "123 Main St"}
    return JsonResponse(jsonData)




def dJournalEdit(request, pk):
    #(to Show Quotation to edit)
    pk = int(pk)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2. Read Journals.csv File ------------------------------------------
  ### =========================================================================
    ###pk = 2300006
    fPath = "Data/" +coFolder+ "/" +Year+ "/C1_Gl/Journals/Journals.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    ### Filter the data by type ie 'ji'-------------------------
    df = df[df['Type'] == 'jl']

    ### file doesn't recongnize date formate first convert into date and than strftime
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    df = df[df['Ref'] == pk].fillna(0) ### Filter as per 'pk' selected quote

    df['unique'] =  df['Ref'].astype(str)+" "+df['accCode'].astype(str)  ### Create a Unique Column

    ### Remove Duplicate Quote and Deleted Record...
    df = df.drop_duplicates(subset=['unique'], keep='last')
    df = df.drop(df.loc[df['action']=='Deleted'].index)


  ### Step 3 - Convert Data into Dictionary -----------------------------------
  ### =========================================================================
    Data = df.to_dict(orient="records")




  ### Step 2 - Read DropDown.csv - to Get the list of Countries and Departments etc--
  ### ===============================================================================
    fPath = "Data/" +coFolder+ "/C1_Gl/DropDown/DropDown.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    Country = df[df['Type'] == 'Country']
    countryList = Country['Description'].tolist()

    Department = df[df['Type'] == 'Department']
    departmentList = Department['Description'].tolist()

    Brand = df[df['Type'] == 'Brand']
    brandList = Brand['Description'].tolist()

    context = {'lastOrder': pk, 'Data':Data,
               'countryList':countryList, 'departmentList':departmentList, 'brandList':brandList,
               }
    return render(request, 'C1_Gl/dJournalEdit.html', context)




def cCOA_List(request):

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    coFolder = str(dfStd.loc[0, 'coFolder'])
    Year = str(dfStd.loc[0, 'year'])


  ### Step 2 - Read DropDown.csv - to Get the list of Countries and Departments etc--
  ### ===============================================================================
    fPath = "Data/" +coFolder+ "/C1_Gl/mergeTB.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape')

    selCol = df[['code', 'head', 'level2']]
    selCol = selCol.replace(r'^.. ', '', regex=True)    # Replace "1. " with ""


    ### Convert Data into Json Dictionary
    Data = selCol.to_dict(orient="records")


    return JsonResponse(Data, safe=False) 


#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ TEST  ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def expend(request):
    context = {'abc':'abc', }
    return render(request, 'C1_Gl/expend.html', context)
