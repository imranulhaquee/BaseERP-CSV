from django.urls import path
from .import views

urlpatterns = [
    path('aPurchasesModule', views.aPurchasesModule, name='aPurchasesModule'),
    path('aSupplierList', views.aSupplierList, name='aSupplierList'),
    path('aSupRefresh', views.aSupRefresh, name='aSupRefresh'),
    
    path('supBasInfo', views.supBasInfo, name='supBasInfo'),
    
    path('showSupp', views.showSupp, name='showSupp'),
    path('addSupplier', views.addSupplier, name='addSupplier'),
    path('addSupp', views.addSupp, name='addSupp'),
    path('aEditSupplier/<str:pk>/', views.aEditSupplier , name='aEditSupplier'),
    path('editSup', views.editSup , name='editSup'),
    path('delSup/<str:pk>/', views.delSup, name='delSup'),


    #═══ Purchase Order ════════════════════════════════════════════════════
    path('pOderList/', views.pOderList, name='pOderList'),
    path('pOrderShow/', views.pOrderShow, name='pOrderShow'),


    path('pOrderAdd/', views.pOrderAdd, name='pOrderAdd'),
    path('pOrderAddUrl', views.pOrderAddUrl, name='pOrderAddUrl'),


    path('supListURL', views.supListURL, name='supListURL'),




    path('zUploadSupData', views.zUploadSupData, name='aUploadSupData'),
]
