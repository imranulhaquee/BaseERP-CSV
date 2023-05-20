from import_export import resources
from .models import  triBal


class triBalResource(resources.ModelResource):
    class meta:
        model = triBal

