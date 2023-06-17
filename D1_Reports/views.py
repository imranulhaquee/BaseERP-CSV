from django.shortcuts import render, redirect, HttpResponse
import os


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
from tablib import Dataset
from django.contrib import messages
from django.db import transaction  # for bulk data upload


### --- Get Data from DataBse through Pands --------------
import sqlite3
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///D:/IUH/2. Programming/2. App/1a BaseERP-CSV/db.sqlite3')

# Create your views here.

#☰☰☰ GL Module ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def aReportModule(request):
    context = {'abc':'abc', }
    return render(request, 'D1_Reports/aReportModule.html', context)



#☰☰☰ F1 Sales Report ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def F1_salesTargetEmp(request):
    

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ##--Step 2 - Read Employee- salesTarget.csv File -----------------------
  ##----------------------------------------------------------------------
    fPath = "Data/" +coFolder+ "/" +Year+ "/I1_Hrm/Targets/salesTarget.csv"
    df = pd.read_csv(fPath, index_col=False, encoding='unicode_escape').fillna('')

    df['unique'] = df['empCode'].astype(str)+" "+df['sNo'].astype(str) ### create a unique column

    DataA = df.drop_duplicates(subset=['unique'], keep='last')  ### drop duplicate value
    DataB = DataA.drop(DataA.loc[DataA['action']=='Deleted'].index) ### drop deleted record


  ##--Step 3 - Create Pivot Table - sby Employee-- -----------------------
  ##----------------------------------------------------------------------
    empPT = pd.pivot_table(DataB,index=["empCName","itemDesc"],values=["salesTarget","qty"],aggfunc=np.sum)
    empPT = empPT.reset_index()
    empGBy = empPT.groupby(['empCName']).agg({'salesTarget': 'sum', 'qty': 'sum'}) 
    empGBy.loc['z. Grand Total'] = empGBy.sum()
    empGBy.reset_index(inplace=True)
    empConcat = pd.concat([empPT, empGBy])
    empSort = empConcat.sort_values(['empCName', 'itemDesc'], ascending = [True, True], na_position ='last')
    empSort['itemDesc'] = empSort['itemDesc'].fillna('Total')


  ##--Step 3 - Create Pivot Table - sby Employee-- -----------------------
  ##----------------------------------------------------------------------
    ### Convert into Dictionary--------------------
    empGBy = empGBy[['empCName','salesTarget']]
    t1List = empGBy.values.tolist() ##Convert into List
    mapDic1 = {code: name for code, name in t1List}
    empSort['Total'] = empSort['empCName'].map(mapDic1)
    empSort['Percentage'] = (empSort['salesTarget'] / empSort['Total'])*100

    ### to Hide and Show----------------------------
    empSort['Department'] = empSort['empCName']
    empSort['Vertical'] = empSort['empCName']
    empSort.loc[empSort["itemDesc"] != "Total", ["Vertical"]] = '---' #  rlSort["status"]


    empData=[]
    for i in range(empSort.shape[0]):
            temp=empSort.iloc[i]
            empData.append(dict(temp))


    context = {'empData':empData, }
    return render(request, 'D1_Reports/F1_salesTargetEmp.html', context)



def F1_salesTargetSup(request):
    
  ##--Step 1 - Read CSV files - "Employee Target" ------------------------
  ##----------------------------------------------------------------------
    df = pd.read_csv("Data/2023/I1_Hrm/Employees/empTarget.csv", index_col=False ,encoding='unicode_escape').fillna(0)

    ##--Step 1a - Remove Duplicate Line and Deleted Record----------------
    DataA = df.drop_duplicates(subset=['empCode'], keep='last')
    DataB = DataA.drop(DataA.loc[DataA['comment']=='Delete'].index)

    ##--Step 1b - Combine Employee Code and Transaction Time--------------
    DataB['combined'] = DataB['empCode'].astype(str)+" "+DataB['traDate']


    ##--Step 1c- Select the Combine Column and convert it into a "LIST"---
    List = DataB["combined"] #.tolist()

  ##--Step 2 - Read CSV files - " Employee Target Detail" ----------------
  ##----------------------------------------------------------------------
    df2 = pd.read_csv("Data/2023/I1_Hrm/Employees/empTargetDetail.csv", index_col=False ,encoding='unicode_escape').fillna(0)
    ### Combine Employee Code and Transaction Time.................
    df2['combined'] = df2['empCode'].astype(str)+" "+df2['traDate']


    ##--Step 3a- Filtere the 'Employee Target Detail' by Employee "Target List"---
    filtered_df = df2[df2['combined'].isin(List)]

    ### Convert 'salesTarget' astype to "FLOAT" to avoid error if any numaric value contain float type.
    filtered_df = filtered_df.astype({'salesTarget':'float'})


  ##--Step 4 - Create Pivot Table - by Supplier --------------------------
  ##----------------------------------------------------------------------

    ### Step 4a- Read Item Master Data CSV file Selected Column and convert into List
    req_cols = ['itmCode','supplier']
    Supp = pd.read_csv("Data/H1_Items/Item/ItemMaster.csv", usecols=req_cols, encoding='unicode_escape').fillna(0)
    supList = Supp.values.tolist() ##Convert into List

    ### Step 4b- Map List with Item Code and get Supplier Name -----------
    supDict = {code: name for code, name in supList}
    filtered_df['supplier'] = filtered_df['itemCode'].map(supDict)


    ### PIVOT BY Supplier------------------------------------
    suppPT = pd.pivot_table(filtered_df,index=["supplier","itemDesc"],values=["salesTarget","qty"],aggfunc=np.sum)
    suppPT= suppPT.reset_index()
    suppGBy = suppPT.groupby(['supplier']).agg({'salesTarget': 'sum', 'qty': 'sum'}) 
    suppGBy.loc['z. Grand Total'] = suppGBy.sum()
    suppGBy.reset_index(inplace=True)
    suppConcat = pd.concat([suppPT, suppGBy])
    suppSort = suppConcat.sort_values(['supplier', 'itemDesc'], ascending = [True, True], na_position ='last')
    suppSort['itemDesc'] = suppSort['itemDesc'].fillna('Total')

    ##--Step 4c- Supplier Traget Percentager by ItemTotal ---------------------
    ### Convert into Dictionary--------------------
    suppGBy = suppGBy[['supplier','salesTarget']]
    t2List = suppGBy.values.tolist() ##Convert into List
    mapDic2 = {code: name for code, name in t2List}
    suppSort['Total'] = suppSort['supplier'].map(mapDic2)
    suppSort['Percentage'] = (suppSort['salesTarget'] / suppSort['Total'])*100

    ### to Hide and Show----------------------------
    suppSort['Department'] = suppSort['supplier']
    suppSort['Vertical'] = suppSort['supplier']
    suppSort.loc[suppSort["itemDesc"] != "Total", ["Vertical"]] = '---' #  rlSort["status"]

    supData=[]
    for i in range(suppSort.shape[0]):
            temp=suppSort.iloc[i]
            supData.append(dict(temp))


    context = {'supData':supData, }
    return render(request, 'D1_Reports/F1_salesTargetSup.html', context)



#☰☰☰ B1 Month End Closing ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def updateSalRevenue (request):
    #(Get All the Sales Delivery Detail)

  ### Step 1. Get Company and Year to Load Data ------------------------------
  ### ========================================================================
    dfStd = pd.read_csv('data/basInfo.csv')
    Year = str(dfStd.loc[0, 'year'])
    coFolder = str(dfStd.loc[0, 'coFolder'])


  ### Step 2 - Read siBasic.csv siAddi.csv File ------------------------------
  ### ========================================================================
    basicPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siBasic.csv"
    siBasic = pd.read_csv(basicPath, index_col=False, encoding='unicode_escape').fillna('')

    addiPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Invoices/siAddi.csv"
    siAddi = pd.read_csv(addiPath, index_col=False, encoding='unicode_escape').fillna('')

    ### siBasic Remove Duplicate Invoice and Deleted Record...convert date into standard date formate........
    siBasic = siBasic.drop_duplicates(subset=['siRef'], keep='last')   ### Remove previous record
    siBasic = siBasic.drop(siBasic.loc[siBasic['action']=='Deleted'].index)  ### Remove Deleted row
    siBasic['siDat'] = pd.to_datetime(siBasic['siDat']).dt.strftime('%Y-%m-%d')  ### convert date to standard Date
    siBasic['unique'] = siBasic['siRef'].astype(str)+" "+siBasic['traDate']  ### Creat a unique column


    siAddi["unique"] = siAddi['siRef'].astype(str)+" "+siAddi['traDate']
    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    mergedSi = pd.merge(siAddi, siBasic['unique'], on='unique', how='inner')

    siAddiCom = pd.merge(mergedSi, siBasic[['siRef', 'siDat',  'cusCode', 'cusName', 'spCode', 'spCName', 'dlRef']], on='siRef', how='left')

    siAddiCom['dlRef'] = siAddiCom['dlRef'].astype(int).astype(str) ### convert 2300003.0 to 2300003
    siAddiCom['unique'] = siAddiCom['dlRef'].astype(str)+' '+siAddi['itmCod'].astype(str)
    siAddiCom['Sales'] = siAddiCom['tot']- siAddi['vat']


  ### Step 3 - Read dlBasic.csv dlAddi.csv File ------------------------------
  ### ========================================================================
    req_cols = ['dlRef','traDate','action']
    basicPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlBasic.csv"
    dlBasic = pd.read_csv(basicPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

    req_cols = ['dlRef','itmCod','wac','traDate','action']
    addiPath = "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Deliveries/dlAddi.csv"
    dlAddi = pd.read_csv(addiPath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

    ### siBasic Remove Duplicate Invoice and Deleted Record...convert date into standard date formate........
    dlBasic = dlBasic.drop_duplicates(subset=['dlRef'], keep='last')   ### Remove previous record
    dlBasic = dlBasic.drop(dlBasic.loc[dlBasic['action']=='Deleted'].index)  ### Remove Deleted row
    dlBasic['uniqueA'] = dlBasic['dlRef'].astype(str)+" "+dlBasic['traDate']  ### Creat a unique column


    dlAddi["uniqueA"] = dlAddi['dlRef'].astype(str)+" "+dlAddi['traDate']
    ###---- Merge to filter out those data which Transaction Date is not matching with qotBasic
    mergedDl = pd.merge(dlAddi, dlBasic['uniqueA'], on='uniqueA', how='inner')

    mergedDl['unique'] = mergedDl['dlRef'].astype(str)+' '+mergedDl['itmCod'].astype(str)

    ### Get 'wac' column and merge with  salAddi-----------
    MergedDf = pd.merge(siAddiCom, mergedDl[['unique', 'wac']], on='unique', how='left')


  ### Step 4 - Read ItemSalPrice.csv File ------------------------------------
  ### ========================================================================
    req_cols = ['itmCode','brand','supplier']
    salPricePath = "Data/" +coFolder+ "/" +Year+ "/H1_Items/Items/ItemSalPrice.csv"
    salPrice = pd.read_csv(salPricePath, usecols=req_cols, index_col=False, encoding='unicode_escape').fillna('')

    salPrice = salPrice.rename(columns={'itmCode': 'itmCod'})

    salPrice = salPrice.drop_duplicates(subset=['itmCod'], keep='last')   ### Remove previous record

    ### Get 'wac' column and merge with  salAddi-----------
    Merged = pd.merge(MergedDf,salPrice[['itmCod', 'supplier']], on='itmCod', how='left')
    Merged = Merged.fillna(0)

    ### Save the data in qotStat.csv File...
    statPath =  "Data/" +coFolder+ "/" +Year+ "/F1_Sales/Analysis/Sales Report.csv"
    Merged.to_csv(statPath, index=False)


    jsonData = {"Company": "BaseFR"}
    return JsonResponse(jsonData)







#☰☰☰  ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

def textRep(request):
    ### Read CSV Files in Pandas...........................
    df = pd.read_csv("Data/Z1_uploadData/SalesA.csv").fillna(0)

    ### Return as List
    Data=[]
    for i in range(df.shape[0]):
            temp=df.iloc[i]
            Data.append(dict(temp))

    context = { "Data": Data, }
    return render(request, 'D1_Reports/textRep.html', context)