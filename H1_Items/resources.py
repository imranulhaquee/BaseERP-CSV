from import_export import resources
from .models import  itmBasic, itmExtra, itmLedger


class itmBasicResource(resources.ModelResource):
    class meta:
        model = itmBasic

class itmExtraResource(resources.ModelResource):
    class meta:
        model = itmExtra

class itmExtraResource(resources.ModelResource):
    class meta:
        model = itmLedger