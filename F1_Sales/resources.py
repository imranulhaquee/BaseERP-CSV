from import_export import resources
from .models import  cusBasic, cusExtra, qotBasic, qotAddi, soBasic, soAddi, dlBasic, dlAddi, siBasic, siAddi


class cusBasicResource(resources.ModelResource):
    class meta:
        model = cusBasic

class cusExtraResource(resources.ModelResource):
    class meta:
        model = cusExtra


class qotBasicResource(resources.ModelResource):
    class meta:
        model = qotBasic


class qotAddiResource(resources.ModelResource):
    class meta:
        model = qotAddi


class soBasicResource(resources.ModelResource):
    class meta:
        model = soBasic


class soAddiResource(resources.ModelResource):
    class meta:
        model = soAddi


class dlBasicResource(resources.ModelResource):
    class meta:
        model = dlBasic


class dlAddiResource(resources.ModelResource):
    class meta:
        model = dlAddi


class siBasicResource(resources.ModelResource):
    class meta:
        model = siBasic


class siAddiResource(resources.ModelResource):
    class meta:
        model = siAddi
