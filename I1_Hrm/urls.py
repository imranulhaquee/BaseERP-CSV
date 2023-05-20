from django.urls import path
from .import views

urlpatterns = [
    path('a1_hrmSetup', views.a1_hrmSetup, name='a1_hrmSetup'),
    path('a1_hrmSetupURL', views.a1_hrmSetupURL, name='a1_hrmSetupURL'),

    path('aEmployeeModule', views.aEmployeeModule, name='aEmployeeModule'),
    path('zUploadEmpData', views.zUploadEmpData, name='zUploadEmpData'),
    
    path('aEmployeeList', views.aEmployeeList, name='aEmployeeList'),
    path('aEmpRefresh', views.aEmpRefresh, name='aEmpRefresh'),
    path('showEmp', views.showEmp, name='showEmp'),

    path('empBasInfo', views.empBasInfo, name='empBasInfo'),

    path('addEmployee', views.addEmployee, name='addEmployee'),
    path('addEmpl', views.addEmpl, name='addEmpl'),
    
    path('editEmployee/<str:pk>/', views.editEmployee , name='editEmployee'),
    path('editEmp', views.editEmp , name='editEmp'),

    path('delEmp/<str:pk>/', views.delEmp, name='delEmp'),


    #------- EMPLOYEE TARGET ---------------------------------------------
    path('tEmpTarget', views.tEmpTarget, name='tEmpTarget'),
    path('tEmpTargetURL', views.tEmpTargetURL, name='tEmpTargetURL'), 
    
    path('tEmpTargetEdit', views.tEmpTargetEdit, name='tEmpTargetEdit'), 
    path('tEmpTargetFetchURL/<str:pk>/', views.tEmpTargetFetchURL, name='tEmpTargetFetchURL'), 


    #------- EMPLOYEE SALARY ---------------------------------------------
    path('empSalary', views.empSalary, name='empSalary'),


]
