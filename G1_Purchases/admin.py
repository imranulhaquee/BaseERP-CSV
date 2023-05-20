from django.contrib import admin
from .models import supBasic, supExtra
from import_export.admin import ImportExportModelAdmin


#☰☰☰ Models ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

# Register your models here.
class supBasicAdmin(admin.ModelAdmin):
    list_display = ('id','supCode', 'supName', 'supActive')

class supExtraAdmin(admin.ModelAdmin):
    list_display = ('id','supCode', 'supPhone', 'supEmail', 'supWeb')




#☰☰☰ Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

admin.site.register(supBasic, supBasicAdmin)
admin.site.register(supExtra, supExtraAdmin)