from django.contrib import admin
from .models import empBasic, empExtra
from import_export.admin import ImportExportModelAdmin



#☰☰☰ Models ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

# Register your models here.

class empBasicAdmin(admin.ModelAdmin):
    list_display = ('id','empCode', 'empFName', 'empStat')

class empExtraAdmin(admin.ModelAdmin):
    list_display = ('id','empCode', 'empPosi', 'empDept', 'empRepTo')



#☰☰☰ Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

admin.site.register(empBasic, empBasicAdmin)
admin.site.register(empExtra, empExtraAdmin)
