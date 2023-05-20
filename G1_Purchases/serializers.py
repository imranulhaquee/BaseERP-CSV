from rest_framework import serializers
from .models import supBasic, supExtra



class supInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = supBasic
        fields = ['id', 'supCode', 'supName']
        #fields = '__all__'

class supBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = supBasic
        #fields = ['id', 'supCode', 'supName', 'opeBal','cloBal','supActive']
        fields = '__all__'

class supExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = supExtra
        fields = '__all__'

