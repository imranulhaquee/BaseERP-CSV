from django.urls import path
from .import views

urlpatterns = [
    path('a2_salesDB', views.a2_salesDB, name='a2_salesDB'),


    #═══ Customer Master File ════════════════════════════════════
    path('a1_salSetup', views.a1_salSetup, name='a1_salSetup'),
    
    #═══ Customer Master File ════════════════════════════════════
    path('aSalesModule', views.aSalesModule, name='aSalesModule'),
    path('aCustomers', views.aCustomers, name='aCustomers'),
    path('aCusRefresh', views.aCusRefresh, name='aCusRefresh'),

    path('cusListURL', views.cusListURL, name='cusListURL'),   

    path('cusBasInfo', views.cusBasInfo, name='cusBasInfo'),
    
    path('showCust', views.showCust, name='showCust'),
    path('cusSelInfo', views.cusSelInfo, name='cusSelInfo'),
    path('lastQuot', views.lastQuot, name='lastQuot'),

    path('addCustomer', views.addCustomer, name='addCustomer'),
    path('addCust', views.addCust, name='addCust'),
    path('aEditCustomer/<str:pk>/', views.aEditCustomer , name='aEditCustomer'),
    path('editCus', views.editCus , name='editCus'),
    path('delCus/<str:pk>/', views.delCus, name='delCus'),

    path('zUploadCusData', views.zUploadCusData, name='aUploadCusData'),
    

    #═══ Sales Quotation ═════════════════════════════════════════════
    path('sQuotList', views.sQuotList, name='sQuotList'),
    path('showQuot', views.showQuot, name='showQuot'),
    path('syncQuot', views.syncQuot, name='syncQuot'),

    path('sQuotAdd/', views.sQuotAdd, name='sQuotAdd'),
    path('sQuotAddUrl', views.sQuotAddUrl, name='sQuotAddUrl'),

    path('sQuotEdit/<str:pk>/', views.sQuotEdit , name='sQuotEdit'),
    path('delQot/<str:pk>/', views.delQot, name='delQot'),
    path('sQuotPdf', views.sQuotPdf, name='sQuotPdf'),
    path('showQuotSum', views.showQuotSum, name='showQuotSum'),


    #═══ Sales Quotation Cost ═══════════════════════════════════════════
    path('sQotCotAdd/<str:pk>/', views.sQotCotAdd, name='sQotCotAdd'),


    #═══ Sales Order ════════════════════════════════════════════════════
    path('sOrderList', views.sOrderList, name='sOrderList'),
    path('showOrderURL', views.showOrderURL, name='showOrderURL'),
    path('syncOrder', views.syncOrder, name='syncOrder'),   

    path('sOrderAdd', views.sOrderAdd, name='sOrderAdd'),
    path('sQuotOpnList', views.sQuotOpnList, name='sQuotOpnList'),
    path('sQuotDetail/<str:pk>/', views.sQuotDetail, name='sQuotDetail'),
    path('sOrderAddUrl', views.sOrderAddUrl, name='sOrderAddUrl'),

    path('sOrderEdit/<str:pk>/', views.sOrderEdit , name='sOrderEdit'),
    path('delSOrd/<str:pk>/<str:Qot>/', views.delSOrd, name='delSOrd'),
    path('sOrderPdf', views.sOrderPdf, name='sOrderPdf'),


    #═══ Delivery Notes ══════════════════════════════════════════════════
    path('sDeliveryList', views.sDeliveryList, name='sDeliveryList'),
    path('showDeliveryURL', views.showDeliveryURL, name='showDeliveryURL'),
    path('syncDelivery', views.syncDelivery, name='syncDelivery'),  

    path('sDeliveryAdd', views.sDeliveryAdd, name='sDeliveryAdd'),
    path('sOrderOpnList', views.sOrderOpnList, name='sOrderOpnList'),
    path('sOrderDetail/<str:pk>/', views.sOrderDetail , name='sOrderDetail'),
    path('sDeliveryAddURL', views.sDeliveryAddURL , name='sDeliveryAddURL'),

    path('sDeliveryEdit/<str:pk>/', views.sDeliveryEdit , name='sDeliveryEdit'),
    path('delDelivery/<str:pk>/<str:Ord>/', views.delDelivery, name='delDelivery'),

    path('sDeliveryPdf', views.sDeliveryPdf, name='sDeliveryPdf'),


    #═══ Sales Invoice ═════════════════════════════════════════════════════
    path('sInvoiceList', views.sInvoiceList, name='sInvoiceList'),
    path('showInvoiceURL', views.showInvoiceURL, name='showInvoiceURL'),
    path('syncInvoice', views.syncInvoice, name='syncInvoice'),  

    path('sInvoiceAdd', views.sInvoiceAdd, name='sInvoiceAdd'),
    path('sDeliveryOpnList', views.sDeliveryOpnList, name='sDeliveryOpnList'),
    path('sDeliveryDetail/<str:pk>/', views.sDeliveryDetail , name='sDeliveryDetail'),
    path('sInvoiceAddURL', views.sInvoiceAddURL , name='sInvoiceAddURL'),

    path('sInvoiceEdit/<str:pk>/', views.sInvoiceEdit , name='sInvoiceEdit'),

    path('delInvoice/<str:pk>/<str:dl>/', views.delInvoice, name='delInvoice'),



    #═══ Sales Analysis ═════════════════════════════════════════════════
    path('tInvoiceDD/<str:pk>/', views.tInvoiceDD, name='tInvoiceDD'),



    #═══ Sales Analysis ═════════════════════════════════════════════════
    path('f1_SalesAnalysis', views.f1_SalesAnalysis, name='f1_SalesAnalysis'),


    
]
