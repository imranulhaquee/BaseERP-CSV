from rest_framework import serializers
from .models import stdGrouping



class stdGroupingSerializer(serializers.ModelSerializer):

    class Meta:
        model = stdGrouping
        #fields=('firstname','lastname')           
        fields = '__all__'   
