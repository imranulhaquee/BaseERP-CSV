from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from A1_Admin.models import Accounts

#--------
from rest_framework.response import Response    # to use DRF function base view
from rest_framework.decorators import api_view   # to use DRF function base view

from A1_Admin.serializers import accountsSerializer
from rest_framework import viewsets

#Verification of Email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ Home Page ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def home(request):

    context = {'abc':'abc', }
    return render(request, 'home.html', context)


# Create your views here.
#==============================================================================

#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ User signUp ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
@api_view(['POST'])
def signUp(request):
    re = request.data  #get the data from html form

    list = []
    for q in re.items():
        list.append(q[1]) #convert QueryDict to python list #print(q[1])

    email = list[0]
    password = list[1]
    Access = list[2]

    first_name = '-'
    last_name = '-'
    username = '-'
    user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username) 
    user.access = Access  #update the user object access
    #user.is_active = True  #update the user object with active
    user.save()


    # USER ACTIVATION -------------------------------------------------
    current_site = get_current_site(request)  #we my use different kind of domain that why we use
    domain = str(current_site)  #  will add in python list, str becasue showing error while creating list
    uid = user.pk
    token =  default_token_generator.make_token(user) # creating a token while activating will check token
    name = email.split('@')[0]
    list.append(domain)
    list.append(uid)
    list.append(token)
    list.append(name)
        

    return Response(list)



#------------------------------------------------------------------------------------------------
#=============================== Activate Customer Account ======================================
#------------------------------------------------------------------------------------------------
def activate(request, uidb64, token):
    try:
        user = Accounts._default_manager.get(pk=uidb64)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect ('login')



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ User Login ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            #abc = Accounts.objects.filter(email=email).values()
            #print(abc)
            return redirect ('LP')   
        else:
            return redirect('login')

    return render(request, 'A1_Admin/login.html')



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ User Logout ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    #messages.success(request, 'You are Logged Out')
    return redirect ('login')



#☰☰☰☰☰☰☰☰☰☰☰☰☰☰ forgot Password ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰
def forgotPassword(request):
    return render(request, 'A1_Admin/forgotPassword.html')


@api_view(['POST'])
def forgot(request):
    re = request.data
    email = re['email']
    name = email.split('@')[0]
    if Accounts.objects.filter(email=email).exists():
        user = Accounts.objects.get(email__exact=email)
        #print(user.id) or print(user.pk)
        list=[]
        
        # RESET PASSWORD ----------------------------------------------------------
        current_site = get_current_site(request)  #we my use different kind of domain that why we use
        domain = str(current_site)  #  will add in python list, str becasue showing error while creating list
        uid = user.pk
        token =  default_token_generator.make_token(user) # creating a token while activating will check token

        list.append(email)
        list.append(name)
        list.append(domain)
        list.append(uid)
        list.append(token)

    return Response(list)



#-------------------------------------------------------------------------------------
#=============================== Reset ===============================================
#-------------------------------------------------------------------------------------
def reset(request, uidb64, token):

    try:
        user = Accounts.objects.get(pk__exact=uidb64)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
         user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = user.pk
        return redirect('resetPassword')
    else:
        return redirect('login')


#------------------------------------------------------------------------------------------------
#=================================== ResetPassword ==============================================
#------------------------------------------------------------------------------------------------
def resetPassword(request):
    return render(request, 'A1_Admin/resetPassword.html')


@api_view(['POST'])
def resetPass(request):
    re = request.data
    password = re['password'] 
    confirm_password = re['cPassword']

    if password == confirm_password:
        uid = request.session.get('uid')
        #uid = 52
        user = Accounts.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        return Response(re)
    else:
        return Response(re)






