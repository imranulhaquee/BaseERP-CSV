from django.contrib import admin
from .models import triBal
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class triBalAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'head', 'opening', 'closing')



#☰☰☰ Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

admin.site.register(triBal, triBalAdmin)