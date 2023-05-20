from django.urls import path
from .import views

urlpatterns = [
    path('aItemsModule', views.aItemsModule, name='aItemsModule'),
    
    path('aItemList', views.aItemList, name='aItemList'),
    path('aItmRefresh', views.aItmRefresh, name='aItmRefresh'),
    path('showItem', views.showItem, name='showItem'),
    path('itmSelInfo', views.itmSelInfo, name='itmSelInfo'),


    path('itmBasInfo', views.itmBasInfo, name='itmBasInfo'),

    path('addItem', views.addItem, name='addItem'),
    path('addItm', views.addItm, name='addItm'),

    path('aEditItem/<str:pk>/', views.aEditItem , name='aEditItem'),
    path('editItm', views.editItm , name='editItm'),

    path('delItm/<str:pk>/', views.delItm, name='delItm'),


    path('itemPrice/', views.itemPrice, name='itemPrice'),


    path('sItemLedger', views.sItemLedger, name='sItemLedger'),
    path('sItemLedgerURL/<str:pk>/', views.sItemLedgerURL, name='sItemLedgerURL'),


    path('zUploadItmData', views.zUploadItmData, name='zUploadItmData'),
    path('zUploadItmLedger', views.zUploadItmLedger, name='zUploadItmLedger'),
]
