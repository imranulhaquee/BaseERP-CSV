from django.urls import path
from .import views

urlpatterns = [
    path('aCrmModule', views.aCrmModule, name='aCrmModule'),
    path('aTracker', views.aTracker, name='aTracker'),
    path('meetNotes', views.meetNotes, name='meetNotes'),
    path('aMeetingList', views.aMeetingList, name='aMeetingList'),
    path('showMeeting', views.showMeeting, name='showMeeting'),

    path('meetingEdit/<str:pk>/', views.meetingEdit , name='meetingEdit'),
    #path('sQuotEditUrl', views.sQuotEditUrl, name='sQuotAddUrl'),  #to save Edited Data

    
]
