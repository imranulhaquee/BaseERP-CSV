from django.urls import path
from .import views

urlpatterns = [
    path('aReportModule', views.aReportModule, name='aReportModule'),


    path('F1_salesTargetEmp', views.F1_salesTargetEmp, name='F1_salesTargetEmp'),
    path('F1_salesTargetSup', views.F1_salesTargetSup, name='F1_salesTargetSup'),


    #═══ Month End Closing  ═════════════════════════════════════════════════
    path('updateSalRevenue', views.updateSalRevenue, name='updateSalRevenue'),


    path('textRep', views.textRep, name='textRep'),

]

