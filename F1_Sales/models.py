from django.db import models


# Create your models here.

#--------------------------------------------------------------------
#--------- Customer -------------------------------------------------
#--------------------------------------------------------------------
class cusBasic(models.Model):
    cusCode = models.CharField(max_length=12, unique=True)
    cusName = models.CharField(max_length=100, blank=False)
    opeBal = models.IntegerField(blank=True, null=True, default=0)
    cloBal = models.IntegerField(blank=True, null=True,  default=0)
    cusActive = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.cusName
    

class cusExtra(models.Model):
    cusCode = models.CharField(max_length=12, unique=True)
    cusLogo = models.ImageField(upload_to='images/cusLogo', null=True, blank=True)  #default='Blank.jpg'   ,default='Blank.png' location start from 'media' folder      (upload_to='photos/products')
    cusPhone = models.CharField(max_length=25, blank=True, null=True)
    cusEmail = models.CharField(max_length=100, blank=True, null=True)
    cusWeb = models.CharField(max_length=100, blank=True, null=True)
    cusBillTo = models.CharField(max_length=100, blank=True, null=True)
    cusShipTo = models.CharField(max_length=100, blank=True, null=True)
    cusAcNum = models.CharField(max_length=50, blank=True, null=True)
    cusCrLim = models.IntegerField(blank=True, null=True, default=0)
    cusPytTerm = models.CharField(max_length=100, blank=True, null=True)
    cusBank = models.CharField(max_length=100, blank=True, null=True)

    cusLegName = models.CharField(max_length=100, blank=True, null=True)
    cusTRN = models.CharField(max_length=25, blank=True, null=True)

    cusTP = models.CharField(max_length=50, blank=True, null=True)
    cusTOJ = models.CharField(max_length=50, blank=True, null=True)
    cusCP = models.CharField(max_length=50, blank=True, null=True)
    cusCPN = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.cusCode
    



#--------------------------------------------------------------------
#--------- Sales Quotation ------------------------------------------
#--------------------------------------------------------------------

class qotBasic(models.Model):
    qotRef = models.CharField(max_length=14, unique=True)
    qotDat = models.DateField(blank=True, null=True)
    cusCode = models.CharField(max_length=20, blank=True, null=True)
    cusName = models.CharField(max_length=100, blank=False, null=True)

    qotTBD = models.FloatField(blank=True, null=True, default=0)
    qotTAD = models.FloatField(blank=True, null=True, default=0)
    qotTax = models.FloatField(blank=True, null=True, default=0)
    qotTAT = models.FloatField(blank=True, null=True, default=0)
    shipTo = models.CharField(max_length=100, blank=True, null=True)
    qotComm = models.CharField(max_length=200, blank=True, null=True)
    salPer = models.CharField(max_length=10, blank=True, null=True)
    spName = models.CharField(max_length=100, blank=True, null=True)
    opnClo = models.CharField(max_length=10, blank=True, null=True, default='Open')

    def __str__(self):
        return self.qotRef
    

class qotAddi(models.Model):
    qotRef = models.CharField(max_length=14, unique=False)
    sno = models.CharField(max_length=12)
    itmCode = models.CharField(max_length=12)
    desc= models.CharField(max_length=200, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True, default=0)
    price = models.FloatField(blank=True, null=True, default=0)
    disc = models.FloatField(blank=True, null=True, default=0)
    tot = models.FloatField(blank=True, null=True, default=0)  

    class Meta:
        indexes = [models.Index(fields=['qotRef'])]

    def __str_(self):
        return self.qotRef
    




#--------------------------------------------------------------------
#--------- Sales Order ----------------------------------------------
#--------------------------------------------------------------------

class soBasic(models.Model):
    soRef = models.CharField(max_length=14, unique=True)
    soDat = models.DateField(blank=True, null=True)
    cusCode = models.CharField(max_length=20, blank=True, null=True)
    cusName = models.CharField(max_length=100, blank=False, null=True)

    soTBD = models.FloatField(blank=True, null=True, default=0)
    soTAD = models.FloatField(blank=True, null=True, default=0)
    soTax = models.FloatField(blank=True, null=True, default=0)
    soTAT = models.FloatField(blank=True, null=True, default=0)
    shipTo = models.CharField(max_length=100, blank=True, null=True)
    soComm = models.CharField(max_length=200, blank=True, null=True)
    opnClo = models.CharField(max_length=10, blank=True, null=True, default='Open')
    spName = models.CharField(max_length=100, blank=True, null=True)
    spCode = models.CharField(max_length=10, blank=True, null=True)
    qotRef = models.CharField(max_length=14)
    qotDat = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.soRef
    

class soAddi(models.Model):
    soRef = models.CharField(max_length=14, unique=False)
    sno = models.CharField(max_length=12)
    itmCode = models.CharField(max_length=12)
    desc= models.CharField(max_length=200, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True, default=0)
    price = models.FloatField(blank=True, null=True, default=0)
    disc = models.FloatField(blank=True, null=True, default=0)
    tot = models.FloatField(blank=True, null=True, default=0)  

    class Meta:
        indexes = [models.Index(fields=['soRef'])]

    def __str_(self):
        return self.soRef



#--------------------------------------------------------------------
#--------- Delivery Notes -------------------------------------------
#--------------------------------------------------------------------

class dlBasic(models.Model):
    dlRef = models.CharField(max_length=14, unique=True)
    dlDat = models.DateField(blank=True, null=True)
    cusCode = models.CharField(max_length=20, blank=True, null=True)
    cusName = models.CharField(max_length=100, blank=False, null=True)

    dlTBD = models.FloatField(blank=True, null=True, default=0)
    dlTAD = models.FloatField(blank=True, null=True, default=0)
    dlTax = models.FloatField(blank=True, null=True, default=0)
    dlTAT = models.FloatField(blank=True, null=True, default=0)
    shipTo = models.CharField(max_length=100, blank=True, null=True)
    dlComm = models.CharField(max_length=200, blank=True, null=True)
    opnClo = models.CharField(max_length=10, blank=True, null=True, default='Open')
    spName = models.CharField(max_length=100, blank=True, null=True)
    spCode = models.CharField(max_length=10, blank=True, null=True)
    soRef = models.CharField(max_length=14)
    soDat = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.dlRef
    

class dlAddi(models.Model):
    dlRef = models.CharField(max_length=14, unique=False)
    sno = models.CharField(max_length=12)
    itmCode = models.CharField(max_length=12)
    desc= models.CharField(max_length=200, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True, default=0)
    price = models.FloatField(blank=True, null=True, default=0)
    disc = models.FloatField(blank=True, null=True, default=0)
    tot = models.FloatField(blank=True, null=True, default=0)  

    class Meta:
        indexes = [models.Index(fields=['dlRef'])]

    def __str_(self):
        return self.dlRef



#--------------------------------------------------------------------
#--------- Sales Invoice --------------------------------------------
#--------------------------------------------------------------------

class siBasic(models.Model):
    siRef = models.CharField(max_length=14, unique=True)
    siDat = models.DateField(blank=True, null=True)
    cusCode = models.CharField(max_length=20, blank=True, null=True)
    cusName = models.CharField(max_length=100, blank=False, null=True)

    siTBD = models.FloatField(blank=True, null=True, default=0)
    siTAD = models.FloatField(blank=True, null=True, default=0)
    siTax = models.FloatField(blank=True, null=True, default=0)
    siTAT = models.FloatField(blank=True, null=True, default=0)
    shipTo = models.CharField(max_length=100, blank=True, null=True)
    siComm = models.CharField(max_length=200, blank=True, null=True)
    opnClo = models.CharField(max_length=10, blank=True, null=True, default='Open')
    spName = models.CharField(max_length=100, blank=True, null=True)
    spCode = models.CharField(max_length=10, blank=True, null=True)
    dlRef = models.CharField(max_length=14)
    dlDat = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.siRef
    

class siAddi(models.Model):
    siRef = models.CharField(max_length=14, unique=False)
    sno = models.CharField(max_length=12)
    itmCode = models.CharField(max_length=12)
    desc= models.CharField(max_length=200, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True, default=0)
    price = models.FloatField(blank=True, null=True, default=0)
    disc = models.FloatField(blank=True, null=True, default=0)
    tot = models.FloatField(blank=True, null=True, default=0)  

    class Meta:
        indexes = [models.Index(fields=['siRef'])]

    def __str_(self):
        return self.dlRef

