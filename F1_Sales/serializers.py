from rest_framework import serializers
from .models import cusBasic, cusExtra, qotBasic, qotAddi, soBasic, soAddi, dlBasic, dlAddi, siBasic, siAddi



class cusInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = cusBasic
        fields = ['id', 'cusCode', 'cusName']
        #fields = '__all__'

class cusBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = cusBasic
        #fields = ['id', 'cusCode', 'cusName', 'opeBal','cloBal','cusActive']
        fields = '__all__'

class cusExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = cusExtra
        fields = '__all__'

class qotBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = qotBasic
        fields = '__all__'

class qotAddiSerializer(serializers.ModelSerializer):
    class Meta:
        model = qotAddi
        fields = '__all__'

class soBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = soBasic
        fields = '__all__'

class soAddiSerializer(serializers.ModelSerializer):
    class Meta:
        model = soAddi
        fields = '__all__'

class dlBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = dlBasic
        fields = '__all__'

class dlAddiSerializer(serializers.ModelSerializer):
    class Meta:
        model = dlAddi
        fields = '__all__'

class siBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = siBasic
        fields = '__all__'

class siAddiSerializer(serializers.ModelSerializer):
    class Meta:
        model = siAddi
        fields = '__all__'

