from django.urls import path
from .import views

urlpatterns = [
    path('a1_hrmSetup', views.a1_hrmSetup, name='a1_hrmSetup'),
    path('a1_hrmSetupURL', views.a1_hrmSetupURL, name='a1_hrmSetupURL'),

    path('a3_EmployeeModule', views.a3_EmployeeModule, name='a3_EmployeeModule'),
    path('zUploadEmpData', views.zUploadEmpData, name='zUploadEmpData'),


    #═══ EMPLOYEE MASTER DATA ════════════════════════════════════════════
    path('mEmpMasterList', views.mEmpMasterList, name='mEmpMasterList'),
    path('mEmpMasterShow', views.mEmpMasterShow, name='mEmpMasterShow'),
    path('syncEmpMaster', views.syncEmpMaster, name='syncEmpMaster'),
    path('mEmpMasterAdd', views.mEmpMasterAdd, name='mEmpMasterAdd'),
    path('mEmpMasterAddUrl', views.mEmpMasterAddUrl, name='mEmpMasterAddUrl'),
    path('mEmpMasterEdit/<str:pk>/', views.mEmpMasterEdit , name='mEmpMasterEdit'),
    path('mEmpMasterDelete/<str:pk>/', views.mEmpMasterDelete, name='mEmpMasterDelete'),

    path('empBasInfo', views.empBasInfo, name='empBasInfo'),

    #═══ EMPLOYEE TARGET ═════════════════════════════════════════════════
    path('tEmpTargetList', views.tEmpTargetList, name='tEmpTargetList'),
    path('syncEmpTarget', views.syncEmpTarget, name='syncEmpTarget'),
    path('tEmpTargetAdd', views.tEmpTargetAdd, name='tEmpTargetAdd'),
    path('tEmpTargetURL', views.tEmpTargetURL, name='tEmpTargetURL'), 
    path('tEmpTargetEdit/<str:pk>/', views.tEmpTargetEdit, name='tEmpTargetEdit'), 
    path('tEmpTargetDelete/<str:pk>/', views.tEmpTargetDelete, name='tEmpTargetDelete'),


    #═══ EMPLOYEE SALARY ═════════════════════════════════════════════════
    path('empSalary', views.empSalary, name='empSalary'),


]
