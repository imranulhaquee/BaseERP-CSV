from django.contrib import admin
from .models import itmBasic, itmExtra, itmLedger
from import_export.admin import ImportExportModelAdmin


#☰☰☰ Models ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

# Register your models here.
class itmBasicAdmin(admin.ModelAdmin):
    list_display = ('id','itmCode', 'itmName', 'itmActive')

class itmExtraAdmin(admin.ModelAdmin):
    list_display = ('id','itmCode', 'brand', 'supplier', 'bisUnit')


class itmLedgerAdmin(admin.ModelAdmin):
    list_display = ('id','itmCode', 'itmName', 'costTOT', 'WAC')


#☰☰☰ Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

admin.site.register(itmBasic, itmBasicAdmin)
admin.site.register(itmExtra, itmExtraAdmin)
admin.site.register(itmLedger, itmLedgerAdmin)