from django.shortcuts import render, redirect



# Create your views here.
def IUH_LP(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/IUH_LP.html', context)


 # -----------
    #dfd
 # ----------

def IUH(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/IUH.html', context)


def test1(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/test1.html', context)



def grid(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/grid.html', context)


def DB1(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/DB1.html', context)


def DB2(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/DB2.html', context)


def DB3(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/DB3.html', context)


def DB4(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/DB4.html', context)



def lpTest(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/lpTest.html', context)

def homeA(request):

    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/homeA.html', context)



def locationTracker(request):
    context = {'abc':'abc', }
    return render(request, 'P1_Portfolio/locationTracker.html', context)