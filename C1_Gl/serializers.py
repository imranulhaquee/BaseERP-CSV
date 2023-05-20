from rest_framework import serializers
from .models import triBal



class triBalSerializer(serializers.ModelSerializer):
    class Meta:
        model = triBal
        fields = '__all__'

