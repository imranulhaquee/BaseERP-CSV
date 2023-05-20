from django.db import models


# Create your models here.
class empBasic(models.Model):
    empCode = models.CharField(max_length=12, unique=True)
    empFName = models.CharField(max_length=20, blank=False)
    empMName = models.CharField(max_length=20, blank=True, null=True)
    empLName = models.CharField(max_length=20, blank=False)
    empStat = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.empFName
    

class empExtra(models.Model):
    empCode  = models.CharField(max_length=12, unique=True)
    empImg = models.ImageField(upload_to='images/empImg', null=True, blank=True)  #default='Blank.jpg'   ,default='Blank.png' location start from 'media' folder      (upload_to='photos/products')
    empPosi = models.CharField(max_length=60, blank=True, null=True)
    empDoj = models.DateField(blank=True, null=True, default='2000-01-01')
    empEid = models.CharField(max_length=30, blank=True, null=True)
    empLoca = models.CharField(max_length=40, blank=True, null=True)
    empDept = models.CharField(max_length=40, blank=True, null=True)
    empRepTo = models.CharField(max_length=30, blank=True, null=True)
    empSpon = models.CharField(max_length=60, blank=True, null=True)

    empNatl= models.CharField(max_length=20, blank=True, null=True)
    empGend = models.CharField(max_length=10, blank=True, null=True)
    empDob = models.DateField(blank=True, null=True, default='2000-01-01')
    EmpMarr = models.CharField(max_length=10, blank=True, null=True)

    empIban= models.CharField(max_length=30, blank=True, null=True)
    empBank= models.CharField(max_length=40, blank=True, null=True)
    empAcc= models.CharField(max_length=20, blank=True, null=True)
    empUid= models.CharField(max_length=20, blank=True, null=True)
    empVisa= models.CharField(max_length=20, blank=True, null=True)

    empAdd= models.CharField(max_length=50, blank=True, null=True)
    empPh= models.CharField(max_length=20, blank=True, null=True)
    empEmail= models.CharField(max_length=35, blank=True, null=True)
    ref= models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.empCode