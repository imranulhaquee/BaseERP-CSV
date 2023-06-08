from django.urls import path
from .import views

urlpatterns = [
    path('aGlModule', views.aGlModule, name='aGlModule'),

    path('CoA', views.CoA, name='CoA'),

    path('aTrialBalance', views.aTrialBalance, name='aTrialBalance'),
    path('showTb', views.showTb, name='showTb'),


    path('CoAEdit/<str:pk>/', views.CoAEdit , name='CoAEdit'),
    #path('editSup', views.editSup , name='editSup'),


    #═════════════ Journal Ledger ════════════════════════════════════ 
    path('TrialBalance', views.TrialBalance , name='TrialBalance'),


    path('syncGenLeger', views.syncGenLeger , name='syncGenLeger'),

    path('sLedger/<str:pk>/', views.sLedger , name='sLedger'),



    path('zUploadTbData', views.zUploadTbData, name='zUploadTbData'),
    


    #═════════════ Expend/Collaps ════════════════════════════════════
    path('expend', views.expend, name='expend'),
]

