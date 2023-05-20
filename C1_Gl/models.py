from django.db import models

# Create your models here.

class triBal(models.Model):  #Chart of Accounts
    code = models.CharField(max_length=20, unique=True, blank=False)
    head = models.CharField(max_length=200, blank=False)
    level1 = models.CharField(max_length=50, blank=False)
    level2 = models.CharField(max_length=50, blank=False)
    level3 = models.CharField(max_length=80, blank=False)
    level4 = models.CharField(max_length=80, blank=False)
    opening = models.FloatField(blank=True, null=True, default=0)
    debit = models.FloatField(blank=True, null=True, default=0)
    credit = models.FloatField(blank=True, null=True, default=0)
    closing = models.FloatField(blank=True, null=True, default=0)


    def __str__(self):
        return self.code