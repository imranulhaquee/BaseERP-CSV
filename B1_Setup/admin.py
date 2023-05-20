from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import stdGrouping


# Register your models here.
class stdGroupingAdmin(admin.ModelAdmin):
    list_display = ('level1', 'level2', 'level3' ,'head')


admin.site.register(stdGrouping, stdGroupingAdmin)
