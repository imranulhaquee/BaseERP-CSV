from django.contrib import admin
from .models import cusBasic, cusExtra, qotBasic, qotAddi , soBasic, soAddi , dlBasic, dlAddi , siBasic, siAddi
from import_export.admin import ImportExportModelAdmin


#☰☰☰ Models ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

# Register your models here.
class cusBasicAdmin(admin.ModelAdmin):
    list_display = ('id','cusCode', 'cusName', 'cusActive')

class cusExtraAdmin(admin.ModelAdmin):
    list_display = ('id','cusCode', 'cusPhone', 'cusEmail', 'cusWeb')

class qotBasicAdmin(admin.ModelAdmin):
    list_display = ('id','qotRef', 'qotDat', 'cusCode')

class qotAddiAdmin(admin.ModelAdmin):
    list_display = ('id','qotRef', 'desc', 'tot')

class soBasicAdmin(admin.ModelAdmin):
    list_display = ('id','soRef', 'soDat', 'cusCode')

class soAddiAdmin(admin.ModelAdmin):
    list_display = ('id','soRef', 'desc', 'tot')

class dlBasicAdmin(admin.ModelAdmin):
    list_display = ('id','dlRef', 'dlDat', 'cusCode')

class dlAddiAdmin(admin.ModelAdmin):
    list_display = ('id','dlRef', 'desc', 'tot')

class siBasicAdmin(admin.ModelAdmin):
    list_display = ('id','siRef', 'siDat', 'cusCode')

class siAddiAdmin(admin.ModelAdmin):
    list_display = ('id','siRef', 'desc', 'tot')




#☰☰☰ Register ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰

admin.site.register(cusBasic, cusBasicAdmin)
admin.site.register(cusExtra, cusExtraAdmin)
admin.site.register(qotBasic, qotBasicAdmin)
admin.site.register(qotAddi, qotAddiAdmin)
admin.site.register(soBasic, soBasicAdmin)
admin.site.register(soAddi, soAddiAdmin)
admin.site.register(dlBasic, dlBasicAdmin)
admin.site.register(dlAddi, dlAddiAdmin)
admin.site.register(siBasic, siBasicAdmin)
admin.site.register(siAddi, siAddiAdmin)
