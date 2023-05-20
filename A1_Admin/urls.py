from django.urls import path
from .import views

urlpatterns = [
    path('abc', views.home, name='home'),
    path('signUp', views.signUp , name='signUp'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login', views.login, name='login'),
    path('logout', views.logout , name='logout'),

    path('forgotPassword', views.forgotPassword , name='forgotPassword'),
    path('forgot', views.forgot , name='forgot'),
    path('reset/<uidb64>/<token>/', views.reset, name='reset'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('resetPass', views.resetPass, name='resetPass'),

]
