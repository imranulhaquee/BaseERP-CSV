from import_export import resources
from .models import  empBasic, empExtra


class empBasicResource(resources.ModelResource):
    class meta:
        model = empBasic

class empExtraResource(resources.ModelResource):
    class meta:
        model = empExtra

