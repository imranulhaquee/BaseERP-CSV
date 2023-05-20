from import_export import resources
from .models import  supBasic, supExtra


class supBasicResource(resources.ModelResource):
    class meta:
        model = supBasic

class supExtraResource(resources.ModelResource):
    class meta:
        model = supExtra

