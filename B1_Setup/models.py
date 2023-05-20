from django.db import models

# Create your models here.

class stdGrouping(models.Model):  #Chart of Accounts
    level1 = models.CharField(max_length=30, blank=False)
    level2 = models.CharField(max_length=30, blank=False)
    level3 = models.CharField(max_length=60, blank=False)
    level4 = models.CharField(max_length=60, blank=False)
    code = models.CharField(max_length=20, unique=True, blank=False)
    head = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.code