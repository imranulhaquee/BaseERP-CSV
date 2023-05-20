from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('LP', views.LP, name='LP'),

    path('UploadStdGrouping', views.UploadStdGrouping , name='UploadStdGrouping'),

]
