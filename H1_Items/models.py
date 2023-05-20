from django.db import models


# Create your models here.
class itmBasic(models.Model):
    itmCode = models.CharField(max_length=12, unique=True)
    itmName = models.CharField(max_length=100, blank=False)
    opeQty = models.IntegerField(blank=True, null=True, default=0)
    cloQty = models.IntegerField(blank=True, null=True,  default=0)
    itmActive = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.itmName
    

class itmExtra(models.Model):
    itmCode = models.CharField(max_length=12, unique=True)
    itmLogo = models.ImageField(upload_to='images/itmLogo', null=True, blank=True)  #default='Blank.jpg'   ,default='Blank.png' location start from 'media' folder      (upload_to='photos/products')
    uPrice = models.IntegerField(blank=True, null=True, default=0)
    brand = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    barCode = models.CharField(max_length=30, blank=True, null=True)
    uom = models.CharField(max_length=30, blank=True, null=True)

    min = models.IntegerField(blank=True, null=True, default=0)
    max = models.IntegerField(blank=True, null=True, default=0)
    roQty = models.IntegerField(blank=True, null=True, default=0)
    discount = models.IntegerField(blank=True, null=True, default=0)

    taxable = models.CharField(max_length=50, blank=True, null=True)
    input = models.IntegerField(blank=True, null=True, default=0)
    output = models.IntegerField(blank=True, null=True, default=0)

    bisUnit = models.CharField(max_length=50, blank=True, null=True)
    itmType = models.CharField(max_length=50, blank=True, null=True)
    expiry = models.IntegerField(blank=True, null=True, default=0)
    ref = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.itmCode
    


    # Create your models here.
class itmLedger(models.Model):
    itmCode = models.CharField(max_length=12)
    itmName = models.CharField(max_length=100, blank=False)
    traDat = models.DateField(blank=True, null=True)
    qtyPU = models.IntegerField(blank=True, null=True, default=0)

    costPU = models.IntegerField(blank=True, null=True, default=0)
    qtyTOT = models.IntegerField(blank=True, null=True, default=0)
    costTOT = models.IntegerField(blank=True, null=True, default=0)
    WAC = models.IntegerField(blank=True, null=True, default=0)
    desc = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=['itmCode'])]

    def __str__(self):
        return self.itmCode