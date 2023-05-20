from django.db import models


# Create your models here.
class supBasic(models.Model):
    supCode = models.CharField(max_length=12, unique=True)
    supName = models.CharField(max_length=100, blank=False)
    opeBal = models.IntegerField(blank=True, null=True, default=0)
    cloBal = models.IntegerField(blank=True, null=True,  default=0)
    supActive = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.supName
    

class supExtra(models.Model):
    supCode = models.CharField(max_length=12, unique=True)
    supLogo = models.ImageField(upload_to='images/supLogo', null=True, blank=True)  #default='Blank.jpg'   ,default='Blank.png' location start from 'media' folder      (upload_to='photos/products')
    supPhone = models.CharField(max_length=25, blank=True, null=True)
    supEmail = models.CharField(max_length=100, blank=True, null=True)
    supWeb = models.CharField(max_length=100, blank=True, null=True)
    supBillFrom = models.CharField(max_length=100, blank=True, null=True)
    supShipFrom = models.CharField(max_length=100, blank=True, null=True)
    supAcNum = models.CharField(max_length=50, blank=True, null=True)
    supCrLim = models.IntegerField(blank=True, null=True, default=0)
    supPytTerm = models.CharField(max_length=100, blank=True, null=True)
    supBank = models.CharField(max_length=100, blank=True, null=True)

    supLegName = models.CharField(max_length=100, blank=True, null=True)
    supTRN = models.CharField(max_length=25, blank=True, null=True)

    supTP = models.CharField(max_length=50, blank=True, null=True)
    supTOJ = models.CharField(max_length=50, blank=True, null=True)
    supCP = models.CharField(max_length=50, blank=True, null=True)
    supCPN = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.supCode