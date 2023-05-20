from rest_framework import serializers
from .models import itmBasic, itmExtra, itmLedger



class itmInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = itmBasic
        fields = ['id', 'itmCode', 'itmName']
        #fields = '__all__'

class itmBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = itmBasic
        fields = '__all__'

class itmExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = itmExtra
        fields = '__all__'


class itmLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = itmLedger
        fields = '__all__'