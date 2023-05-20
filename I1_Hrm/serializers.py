from rest_framework import serializers
from .models import empBasic, empExtra


class empInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = empBasic
        fields = ['id', 'empCode', 'empFName']
        #fields = '__all__'

class empBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = empBasic
        fields = '__all__'

class empExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = empExtra
        fields = '__all__'

