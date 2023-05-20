from django.contrib import admin
from django.urls import path, include  #include is to rout urls to app urls.
from django.conf.urls.static import static  
from django.conf import settings   #because we made some changes i.e. media root etc

from rest_framework import routers 
route = routers.DefaultRouter()

urlpatterns = [
    path('adminBoard/', admin.site.urls),
    path('', include('A1_Admin.urls')),   #will show errors untill we create urls.py under “Admin App”
    path('', include('B1_Setup.urls')),
    path('', include('C1_Gl.urls')),
    path('', include('D1_Reports.urls')),
    path('', include('F1_Sales.urls')),
    path('', include('G1_Purchases.urls')),
    path('', include('H1_Items.urls')),
    path('', include('I1_Hrm.urls')),
    path('', include('O1_Crm.urls')),
    path('', include('P1_Portfolio.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
