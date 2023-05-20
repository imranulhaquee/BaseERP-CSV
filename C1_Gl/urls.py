from django.urls import path
from .import views

urlpatterns = [
    path('aGlModule', views.aGlModule, name='aGlModule'),

    path('CoA', views.CoA, name='CoA'),

    path('aTrialBalance', views.aTrialBalance, name='aTrialBalance'),
    path('showTb', views.showTb, name='showTb'),


    path('CoAEdit/<str:pk>/', views.CoAEdit , name='CoAEdit'),
    #path('editSup', views.editSup , name='editSup'),

    path('zUploadTbData', views.zUploadTbData, name='zUploadTbData'),
]

