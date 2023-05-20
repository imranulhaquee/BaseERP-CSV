from django.urls import path
from .import views

urlpatterns = [
    path('IUH_LP', views.IUH_LP, name='IUH_LP'),
    path('IUH', views.IUH, name='IUH'),
    path('test1', views.test1, name='test1'),
    path('grid', views.grid, name='grid'),
    
    path('DB1', views.DB1, name='DB1'),
    path('DB2', views.DB2, name='DB2'),
    path('DB3', views.DB3, name='DB3'),
    path('DB4', views.DB4, name='DB4'),

    path('lpTest', views.lpTest, name='lpTest'),
    path('homeA', views.homeA, name='homeA'),
    
    path('locationTracker', views.locationTracker, name='locationTracker'),

]
